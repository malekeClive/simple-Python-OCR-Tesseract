#---------- Module ----------#
from flask import Flask, jsonify, request, send_from_directory
import pymysql
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd
from PIL import Image
import pytesseract
import db_config
import time


app = Flask(__name__)
app.config['file_allowed'] = ['image/png', 'image/jpeg']
app.config['image_storage'] = path.join(getcwd(), 'image_storage')

@app.route('/', methods=['GET'])
def index():
    try:
        conn = db_config.mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM file')
        rows = cursor.fetchall()
        if rows == ():
            return jsonify( status = 'OK',
                            results = "No Data",
                            error = None
                            ), 200
        else:
            return jsonify( status = 'OK',
                            results = rows,
                            error = None
                            ), 200

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/v1/upload', methods=['POST'])
def upload():
    try:
        img_form = request.files['filename']
        filename = str(time.time()) + "_" + secure_filename(img_form.filename)
        local_storage = path.join(app.config['image_storage'])
        img_form.save(path.join(local_storage, filename))
        convert = pytesseract.image_to_string(Image.open(path.join(local_storage, filename)))
        print(convert)

        # sql command
        conn = db_config.mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sql = "INSERT INTO file (path, description) VALUES (%s, %s)"
        value = (filename, convert)
        cursor.execute(sql, value)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify( status = 'OK',
                        msg = 'Saved',
                        data = filename,
                        error = None
                        ), 201
    except Exception as e:
        print(e)
        return jsonify( status = 'FAILED',
                        msg = 'failed',
                        data = 'no data saved',
                        error = True
                        ), 422

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['image_storage'],
                               filename)

#----------- Run the APP ----------#
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'thisissecretkey'
    app.run(debug=True)