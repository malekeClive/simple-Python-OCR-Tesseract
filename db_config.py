from app import app
from os import path, getcwd
import pymysql
from flaskext.mysql import MySQL

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'db_ocr'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)