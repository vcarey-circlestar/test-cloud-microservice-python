from flask import Flask, request
import os, logging, json

app = Flask(__name__)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the logging level

# Format logs as JSON
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'message': record.getMessage(),
            'severity': record.levelname,  # Maps to Cloud Logging severity levels
            'name': record.name,  # Optional: Include logger name
        }
        return json.dumps(log_record)

# Create a handler that outputs JSON to stdout
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    logger.info(json.dumps('Hello from my Python endpoint!')) 
    if request.method == 'POST':
        logger.info(json.dumps({'message':'POST'})) 
        return 'This is a POST request'
    return 'Hello, World!'


@app.route('/greet/<name>', methods=['GET'])
def greet(name):
    logger.info(json.dumps('Greetings from a Python endpoint!')) 
    return f'Hi {name}'

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
