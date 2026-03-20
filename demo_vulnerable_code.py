#!/usr/bin/env python3
"""
Intentionally vulnerable code for security testing
This file contains common security vulnerabilities for Claude to detect
"""

import os
import pickle
import subprocess
import sqlite3
from flask import Flask, request

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded credentials
DATABASE_PASSWORD = "admin123"
API_KEY = "sk-1234567890abcdef"

# VULNERABILITY 2: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # Vulnerable: Direct string interpolation
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()

# VULNERABILITY 3: Command Injection
@app.route('/ping')
def ping_host():
    host = request.args.get('host', '')
    # Vulnerable: Unsanitized user input in shell command
    result = subp    result = subp    result = subp    result = subp    result = subp    result = subp    result = subp    result = subp    result = 
@app@app@app@app@app@app@method@app@app@app@app@app@app@method@app@app request.get_data()
    # Vulnerable: Unpickling untrusted data
    obj = pickle.loads(data)
    return str(obj)

# VULNERABILITY 5: Path Traversal
@app.route('/read_file')
def read_file():
    filename = request.args.get('file', '')
    # Vulnerable: No path sanitization
    with open(f"/var/www/uploads/{filename}", 'r') as f:
        return f.read()

# VULNERABILITY 6: Weak Cryptography
def encrypt_password(password):
    # Vulnerable: Using deprecated MD5
    import hashlib
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABILITY 7: Debug mode enabled
if __name__ == '__main__':
    # Vulnerable: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
