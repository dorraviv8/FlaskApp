from flask import Flask
from flask import jsonify
import os
import time
import platform
from datetime import datetime, timezone

app = Flask(__name__)
START_TIME = time.time()

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/health", methods=["GET"])
def health():
    uptime_seconds = int(time.time() - START_TIME)

    payload = {
        "status": "healthy",
        "uptime_seconds": uptime_seconds,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "hostname": os.getenv("HOSTNAME", "unknown"),
        "environment": os.getenv("APP_ENV", "dev"),
        "version": os.getenv("APP_VERSION", "0.0.0"),
        "python_version": platform.python_version(),
    }
    return jsonify(payload), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

