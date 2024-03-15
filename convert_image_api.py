from flask import Flask, request, jsonify
from io import BytesIO
from replit import db
import base64
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_and_get_url(file_or_data):
    if isinstance(file_or_data, bytes):
        filename = 'base64_image.png'
        file_data = base64.b64decode(file_or_data)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'wb') as f:
            f.write(file_data)
        return f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co/{filename}"
    elif hasattr(file_or_data, 'filename') and allowed_file(file_or_data.filename):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_or_data.filename)
        file_or_data.save(file_path)
        return f"https://{os.getenv('REPL_SLUG')}.{os.getenv('REPL_OWNER')}.repl.co/{file_or_data.filename}"
    return None

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files
    if 'image1' not in files or 'image2' not in files:
        return "No files provided"

    image_url1 = save_and_get_url(files['image1'].read())
    image_url2 = save_and_get_url(files['image2'].read())

    images_list = db.get('images', [])
    images_list.extend([image_url1, image_url2])
    db['images'] = images_list

    return "Files uploaded and processed successfully"

@app.route('/get_images', methods=['GET'])
def get_images():
    images_list = db.get('images', [])
    return jsonify(images=images_list)

if __name__ == '__main__':
    app.run(debug=True)
    