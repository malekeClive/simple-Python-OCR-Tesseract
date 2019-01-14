import os
from flask import Flask, request, jsonify, render_template, json
import requests
from flask_sqlalchemy import SQLAlchemy
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
import time
import datetime
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import Img

@app.route('/', methods=['GET'])
def index():
    try:
        # rs = []
        results = Img.query.all()

        # for res in results:
        #     print(res)
        #     rs.append(res)

        value = [e.serialize() for e in results]
        # print(value)
        # print(jsonify([e.serialize() for e in results]))
        return render_template('index.html', values=value)
        # return render_template('index.html', value=values)
    except Exception as e:
        return(str(e))

@app.route('/upload', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        img_form = request.files['filename'] # get form filename
        if img_form:
            filename = str(time.time()) + "_" + secure_filename(img_form.filename) # change filename
            times = datetime.datetime.now().strftime("%d-%m-%y %H:%M") # get current time
            upload_result = upload(img_form) # upload image to cloudinary
            response = requests.get(upload_result['url']) # get image url from upload result
            img_file = Image.open(io.BytesIO(response.content)) # get image from cloudinary
            text = pytesseract.image_to_string(img_file) # convert image to text
            try:
                # save to postgres
                res = Img(
                    path=upload_result['url'],
                    description = text,
                    created_at=times
                )
                db.session.add(res)
                db.session.commit()
                # return jsonify( status = 'OK',
                #                 msg = 'Saved',
                #                 error = None
                #             ), 201
                return render_template('upload.html')
            except Exception as e:
                return(str(e))
        return render_template('upload.html')
        
    return render_template('upload.html')

if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'thisissecretkey'
    app.run()
