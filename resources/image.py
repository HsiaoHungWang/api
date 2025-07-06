from flask_restful import Resource
from flask import send_file, request
from werkzeug.utils import secure_filename

import os
import base64

UPLOAD_FOLDER = os.path.join('static', 'images')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)



class Image(Resource):
    def get(self):
        image_path = os.path.join('static', 'images', 'dog1.jpg')  # 圖片路徑
        return send_file(image_path, mimetype='image/jpeg')

        # return {'message': '讀取圖片'}

    def post(self):
        if 'image' not in request.files:
            return {'message': 'No image file in request'}, 400

        image = request.files['image']
        if image.filename == '':
            return {'message': 'No selected file'}, 400

        filename = secure_filename(image.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        image.save(filepath)

        return {
            'message': 'Image uploaded successfully',
            'url': f'/static/uploads/{filename}'
        }

class Base64Image(Resource):
    def get(self):
        image_path = os.path.join('static', 'images', 'dog1.jpg')

        # 將圖片讀成 base64 字串
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        return {
            "image": image_data,
            "description": "這是一張狗的圖片",
            "format": "jpg"
        }
