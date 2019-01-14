
# Example POST syntax
# curl -F "file=@/home/code/a.pdf" http://127.0.0.1:5000/upload

# Example DELETE syntax
# curl -X DELETE http://127.0.0.1:5000/delete/textfile.txt

# Example PUT (update) syntax
# curl -X PUT -F "file=@/home/code/textfile.txt" http://127.0.0.1:5000/upload

# Example DELETE syntax
# curl -X DELETE http://127.0.0.1:5000/textfile.txt

import os
import shutil
import hashlib
from flask import Flask, request, flash, make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename

STORAGE_FOLDER = '/home/code/http-api/_storage'
TEMP_FOLDER = '/home/code/http-api/_temp'
ALLOWED_EXTENSIONS = set(['txt','json','xml'])
BUF_SIZE = 65536

app = Flask(__name__)
app.config['STORAGE_FOLDER'] = STORAGE_FOLDER
app.config['TEMP_FOLDER'] = TEMP_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST','PUT'])
def upload_file():

    if 'file' not in request.files:
        return make_response(jsonify({"error": "No file part."}), 400)

    file = request.files['file']

    if file.filename == '':
        return make_response(jsonify({"error": "Empty filename."}), 400)
    
    if request.method == 'POST':

        if file.filename in os.listdir(os.path.join(app.config['STORAGE_FOLDER'])):
            return make_response(jsonify({"error": "Duplicate filename in storage."}), 400)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['STORAGE_FOLDER'], file.filename))
            return make_response(jsonify({"result": "File uploaded."}), 200)
        else:
            return make_response(jsonify({"error": "Unrecognized file format."}), 400)

    if request.method == 'PUT':

        if file.filename not in os.listdir(os.path.join(app.config['STORAGE_FOLDER'])):
            return make_response(jsonify({"error": "File does not exist."}), 400)
        else:
            md5_existing = hashlib.md5()
            md5_new = hashlib.md5()

            existing_file = os.path.join(app.config['STORAGE_FOLDER'], file.filename)

            # Find hash of existing file
            with open(existing_file, "rb") as f:
                while True:
                    data = f.read(BUF_SIZE)  # read data as BUF_SIZE byte chunks
                    if not data:
                        break
                    md5_existing.update(data)
            print("MD5: {0}".format(md5_existing.hexdigest()))

            # Copy the file being uploaded into the TEMP_FOLDER directory for processing
            print('saving file in temp directory for processing...')
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['TEMP_FOLDER'], file.filename))

            temp_file = os.path.join(app.config['TEMP_FOLDER'], file.filename)

            # Find hash of file being uploaded
            with open(temp_file, "rb") as f:
                while True:
                    data = f.read(BUF_SIZE)
                    if not data:
                        break
                    md5_new.update(data)
            print("MD5: {0}".format(md5_new.hexdigest()))

            if md5_existing.hexdigest() == md5_new.hexdigest():
                os.remove(temp_file)
                return make_response(jsonify({"result": "No difference between file being uploaded and existing file."}), 200)
            else:
                # Copy the file from temp location and overwrite main storage
                shutil.move(temp_file, existing_file)
                return make_response(jsonify({"result": "File updated."}), 200)

    return make_response(jsonify({"error": "Bad request."}), 400)


@app.route('/<name>', methods=['GET','DELETE'])
def download_file(name):

    if name not in os.listdir(os.path.join(app.config['STORAGE_FOLDER'])):
        return make_response(jsonify({"error": "File does not exist."}), 400)

    if request.method == 'GET':
        return send_from_directory(directory=os.path.join(app.config['STORAGE_FOLDER']), filename = name)

    if request.method == 'DELETE':
        os.remove(os.path.join(app.config['STORAGE_FOLDER'], name))
        return make_response(jsonify({"result": "File deleted."}), 200)

