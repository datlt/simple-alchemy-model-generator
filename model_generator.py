import configparser
import psycopg2
from template_loader import env

def config(filename='config.ini', section='db'):
    parser = configparser.ConfigParser()
    parser.read(filename)

    # db = parser.sections()
    db={}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def get_connection():
    conn = None
    try:
        params = config()
        print("Connecting to Database")
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def get_table_info():
    conn = get_connection()
    cur = conn.cursor()
    select_table_info_query = '''
select json_build_object(
	'table_name', tab.table_name,
    'columns', tab._col ,
    'one_to_many', one_to_many._fk,
    'many_to_one', many_to_one._fk,
    'primary_key', pk_.column_name
)as table_info from (
	select 
		col.table_name as table_name , 
		json_agg(col) as _col
	from information_schema."columns" col  
	where col.table_schema = 'public' group by col.table_name
) as tab
left outer join (
	select one_to_many.table_name as table_name , json_agg(one_to_many) as _fk 
	from
	(SELECT
	    tc.table_schema as table_schema , 
	    tc.constraint_name as constraint_name , 
	    tc.table_name as table_name , 
	    kcu.column_name, 
	    ccu.table_schema AS foreign_table_schema,
	    ccu.table_name AS foreign_table_name,
	    ccu.column_name AS foreign_column_name 
	FROM 
	    information_schema.table_constraints AS tc 
	    JOIN information_schema.key_column_usage AS kcu
	      ON tc.constraint_name = kcu.constraint_name
	      AND tc.table_schema = kcu.table_schema
	    JOIN information_schema.constraint_column_usage AS ccu
	      ON ccu.constraint_name = tc.constraint_name
	      AND ccu.table_schema = tc.table_schema
	WHERE tc.constraint_type = 'FOREIGN KEY') as one_to_many
	group by one_to_many.table_name
) as one_to_many on (one_to_many.table_name = tab.table_name)
left outer join (
	select many_to_one.foreign_table_name as table_name , json_agg(many_to_one) as _fk 
	from
	(SELECT
	    tc.table_schema as table_schema , 
	    tc.constraint_name as constraint_name , 
	    tc.table_name as table_name , 
	    kcu.column_name, 
	    ccu.table_schema AS foreign_table_schema,
	    ccu.table_name AS foreign_table_name,
	    ccu.column_name AS foreign_column_name 
	FROM 
	    information_schema.table_constraints AS tc 
	    JOIN information_schema.key_column_usage AS kcu
	      ON tc.constraint_name = kcu.constraint_name
	      AND tc.table_schema = kcu.table_schema
	    JOIN information_schema.constraint_column_usage AS ccu
	      ON ccu.constraint_name = tc.constraint_name
	      AND ccu.table_schema = tc.table_schema
	WHERE tc.constraint_type = 'FOREIGN KEY') as many_to_one
	group by many_to_one.foreign_table_name
) as many_to_one on (many_to_one.table_name = tab.table_name)
left outer join (
	select tc.table_schema as table_schema , 
		tc.table_name as table_name , 
		kcu.column_name as column_name
	from information_schema.table_constraints as tc 
	join information_schema.key_column_usage as kcu
	ON tc.constraint_name = kcu.constraint_name
	AND tc.table_schema = kcu.table_schema
	where tc.table_schema = 'public' and tc.constraint_type ='PRIMARY KEY'
)as pk_ on (pk_.table_name = tab.table_name);
'''
    cur.execute(select_table_info_query)
    tables_info = cur.fetchall()
    return tables_info

def generate():
    tables_info = get_table_info()
    template = env.get_template("sqlAlchemy_model_template.jinja")
    print("generating model...")
    return template.render(tables_info = tables_info)

def export_output(content):
    output_info = config(section="output")
    with open(output_info["file"], "w") as f:
        f.write(content)
        f.close()
    print("Model is written to file: " + output_info["file"])

def run():
	export_output(generate())

run()

