import os
from flask import Flask, request, session, abort, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import logging
from collections import defaultdict
from getDatas import getDatas, vars
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('HELLO WORLD')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './Data'
CORS(app, expose_headers='Authorization')


@app.route('/upload', methods=['POST'])
def fileUpload():
    target = os.path.join(app.config['UPLOAD_FOLDER'], '')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination = "/".join([target, filename])
    file.save(destination)
    return jsonify(success=True)


@app.route('/variables', methods=['POST'])
def variables():
    global vars
    if not request.json or not 'vihicleMass' in request.json:
        abort(400)
    vars = request.json
    return jsonify(success=True)


@app.route('/test', methods=['GET'])
def test():
    return jsonify(vars)


@app.route('/datas', methods=['GET'])
def get_datas():
    results = getDatas()

    return jsonify(results)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True, port=8000)
