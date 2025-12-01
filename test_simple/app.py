from flask import Flask, jsonify, request

import os, json, io, tempfile

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "circlestar-2024")


                                 
@app.route('/hello_world', methods=['GET'])
def hello_world():
    return "hello world"


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=DB_PORT)
