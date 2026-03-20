"""
Simple vulnerable API for Claude Code security review demo
"""
from flask import Flask, request
import os
import sqlite3

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded API credentials
API_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
DB_PASSWORD = "admin123"

@app.route('/user/<user_id>')
def get_user(user_id):
    # VULNERABILITY 2: SQL Injection
    conn = sqlite3.connect('app.db')
    query = f"SELECT * FROM users WHERE id = {user_id}"
    result = conn.execute(query).fetchall()
    return str(result)

@app.route('/exec')
def execute():
    # VULNERABILITY 3: Command Injection
    cmd = request.args.get('cmd')
    output = os.system(cmd)
    return f"Result: {output}"

if __name__ == '__main__':
    # VULNERABILITY 4: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
