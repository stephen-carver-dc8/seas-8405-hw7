from flask import Flask, request, jsonify
import os
import subprocess
import ast
import re
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Dynamic password
PASSWORD = os.getenv("PASSWORD")

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

# Command injection vulnerability
@app.route('/ping')
def ping():
    ip = request.args.get('ip', '')
    if not re.match(r'^[\d\.]+$', ip):  # Basic IPv4 validation
        return jsonify({"error": "Invalid IP format"}), 400
    try:
        result = subprocess.check_output(["ping", "-c", "1", ip])
        return result
    except Exception as e:
        return jsonify({"error": "Ping failed"}), 500

# Insecure use of eval
@app.route('/calculate')
def calculate():
    expression = request.args.get('expr', '')
    try:
        result = ast.literal_eval(expression)
    except (ValueError, SyntaxError):
        return jsonify({"error": "Invalid expression"}), 400
    return str(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
