from jinja2 import Environment, FileSystemLoader, select_autoescape
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(),
)
env.trim_blocks = True
env.lstrip_blocks = True
def table_name_to_class(tableName):
    tableName = strip_tbl(tableName)
    components = tableName.split('_')
    return ''.join(x.title() for x in components)
def strip_tbl(tableName):
	return tableName.replace("tbl_", "")
def column_type(column_info):
    if column_info["data_type"] == "character varying":
        return "String(" + str(column_info["character_maximum_length"]) + ")"
    elif column_info["data_type"] =="timestamp without time zone":
        return "TIMESTAMP" 
    elif column_info["data_type"] =="text":
        return "Text" 
    elif column_info["data_type"] =="boolean":
        return "Boolean" 
    elif column_info["data_type"] =="numeric":
        return "Numeric" 
    elif column_info["data_type"] =="date":
        return "Date" 
    elif column_info["data_type"] =="integer":
        return "BIGINT" 
    else:
        return column_info["data_type"].upper()  
def nullable(text):
    return "True" if text == "YES" else "False"

enum_columns={
    "tbl_device_config.status": "DeviceConfigStatus",
    "tbl_garages.garage_status": "GarageStatus",
    "tbl_garages.garage_type": "GarageTypes",
    "tbl_users.status": "UserStatus",
    "tbl_locations.loc_status": "TwostateStatus",
}
def insert_label(column_info):
    column_name = column_info["table_name"] + "." + column_info["column_name"]
    if (column_name) in enum_columns:
        return enum_columns[column_name]
    return None

env.filters['table_name_to_class'] = table_name_to_class
env.filters['column_type'] = column_type
env.filters['nullable'] = nullable
env.filters['strip_tbl'] = strip_tbl
env.filters['insert_label'] = insert_label