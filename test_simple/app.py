from flask import Flask, jsonify, request

import os, json, io, tempfile

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "circlestar-2024")

port = int(os.environ.get('PORT', 8080))

app = Flask(__name__)
                                 
@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
