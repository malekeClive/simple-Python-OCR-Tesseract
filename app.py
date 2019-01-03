#---------- Module ----------#
from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from os import path, getcwd
from PIL import Image
import pytesseract

app = Flask(__name__)
app.config['image_storage'] = path.join(getcwd(), 'image_storage')
# db = SQLAlchemy()


@app.route('/', methods=['GET'])
def index():
    print (pytesseract.image_to_string(Image.open('test.png')))
    return('index')

@app.route('/v1/upload', methods=['POST'])
def upload():
    try:
        img_form = request.files['filename']
        filename = secure_filename(img_form.filename)
        local_storage = path.join(app.config['image_storage'])
        img_form.save(path.join(local_storage, filename))
        convert = pytesseract.image_to_string(Image.open(filename))
        print(convert)
        return jsonify( id = 1,
                        status = 'OK',
                        msg = 'Saved',
                        results = filename,
                        error = None
                        ), 201
    except:
        return jsonify( id = 1,
                        status = 'FAILED',
                        msg = 'failed',
                        results = 'no data saved',
                        error = True
                        ), 422


#----------- Run the APP ----------#
if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'thisissecretkey'
    app.run(debug=True)