-------------------------------------------------------------------------------------
It is a tool to generate a model class for SQLAlchemy from DB information.

# How to run
1. Install jinja2 with pip
  $ pip install jinja2
2. Rename the config.ini.template file to config.ini and enter the target DB information.
3. Execute the following command in the `generator` folder
  $ python model_generator.py

# Customize model file
If you want to change the format of the output file, you can modify the following template
templates/sqlAlchemy_model_template.jinja

See the following article for template format
https://jinja.palletsprojects.com/en/3.0.x/templates/ 

Limitations:
　The case where two tables have multiple foreign keys is not yet supported. 
-------------------------------------------------------------------------------------
DBの情報からSQLAlchemyのモデルクラスを生成するツールです
# 実行手順
1．pipでjinja2をインストール
  $ pip install jinja2
2．config.ini.template　ファイルを config.iniにファイル名を変更し、対象ＤＢの情報を入力します
3．generatorフォルダーで以下のコマンドを実行
  $ python model_generator.py

# モデルファイルのカスタマイズ
出力ファイルのフォーマットを変更したい場合は以下のテンプレートファイルを修正できます。
templates/sqlAlchemy_model_template.jinja

テンプレートのフォーマットは以下の記事に参照
https://jinja.palletsprojects.com/en/3.0.x/templates/

制限事項：
　二つのテーブルが複数の外部キーがあるケースはまだ対応しません。

