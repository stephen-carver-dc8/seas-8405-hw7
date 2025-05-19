from flask import Flask, request, jsonify
import os
import subprocess
from pydantic import BaseModel, IPvAnyAddress, constr, ValidationError
from simpleeval import simple_eval, InvalidExpression
from dotenv import load_dotenv

load_dotenv()

# IP Addresses only
class PingRequest(BaseModel):
    ip: IPvAnyAddress

# Constrained string: only alphanumeric, at least 1 character, max 30
class NameRequest(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=30, pattern=r'^[a-zA-Z]+$')

app = Flask(__name__)

# Dynamic password
PASSWORD = os.getenv("PASSWORD")

@app.route('/')
def hello():
    name_param  = request.args.get('name', 'World')
    try:
        validated = NameRequest(name=name_param)
    except ValidationError as e:
        return jsonify({"error": "Invalid name. Must be alphanumeric with no spaces or special characters."}), 400

    return f"Hello, {validated.name}!"

@app.route('/ping')
def ping():

    ip_param = request.args.get('ip', '')
    
    try:
        validated = PingRequest(ip=ip_param)
    except ValidationError as e:
        return jsonify({"error": "Invalid IPv4 address"}), 400

    try:
        result = subprocess.check_output(["ping", "-c", "1", str(validated.ip)], text=True)
        return result
    except Exception as e:
        return jsonify({"error": "Ping failed"}), 500

@app.route('/calculate')
def calculate():
    expression = request.args.get('expr', '')
    try:
        result = simple_eval(expression)
    except (InvalidExpression, ValueError):
        return jsonify({"error": "Invalid expression"}), 400
    return str(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
