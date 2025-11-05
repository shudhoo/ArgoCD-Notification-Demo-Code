from flask import Flask, request, jsonify
import logging
import json
from datetime import datetime

app = Flask(__name__)

# Configure logging to emit JSON-formatted logs
# Flat JSON LOGS
#class JsonFormatter(logging.Formatter):
#    def format(self, record):
#        log_record = {
#            "timestamp": datetime.utcnow().isoformat(),
#            "level": record.levelname.lower(),
#            "message": record.getMessage(),
#            "status_code": getattr(record, "status_code", None),
#            "path": request.path if request else None
#        }
#        return json.dumps(log_record)

# Nested JSON Logs
class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "fields": {
                "level": record.levelname.lower(),
                "message": record.getMessage(),
                "status_code": getattr(record, "status_code", None),
                "path": request.path if request else None
            }
        }
        return json.dumps(log_record)
    
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
app.logger.handlers = [handler]
app.logger.setLevel(logging.INFO)

@app.route('/route1')
def route1():
    app.logger.info("Request complete", extra={"status_code": 200})
    return jsonify({"result": "Route1 OK"}), 200

@app.route('/route2')
def route2():
    app.logger.info("Request complete", extra={"status_code": 404})
    return jsonify({"result": "Route2 Not Found"}), 404

@app.route('/route3')
def route3():
    app.logger.info("Request complete", extra={"status_code": 500})
    return jsonify({"result": "Route3 Server Error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True, )