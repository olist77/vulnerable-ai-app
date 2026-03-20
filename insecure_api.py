#!/usr/bin/env python3
"""
Insecure API endpoints with multiple vulnerabilities
"""

import os
import pickle
import subprocess
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Hardcoded secret - VULNERABILITY
SECRET_KEY = "my-secret-key-12345"
API_TOKEN = "Bearer sk-prod-1234567890abcdef"

@app.route('/api/user/<user_id>')
def get_user(user_id):
    """Get user information - SQL Injection vulnerability"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # VULNERABILITY: SQL Injection via string formatting
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    return jsonify(result)

@app.route('/api/exec')
def execute_command():
    """Execute system command - Command Injection vulnerability"""
    cmd = request.args.get('cmd', 'ls')
    # VULNERABILITY: Command injection via shell=True
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return jsonify({'output': result.stdout, 'error': result.stderr})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """Upload and deserialize file - Insecure Deserialization"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    # VULNERABILITY: Unsafe pickle deserialization
    data = pickle.loads(file.read())
    return jsonify({'data': str(data)})

@app.route('/api/files/<path:filename>')
def read_file(filename):
    """Read file - Path Traversal vulnerability"""
    # VULNERABILITY: No path sanitization allows ../../../etc/passwd
    try:
        with open(f"/var/www/files/{filename}", 'r') as f:
            content = f.read()
        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)}), 404

if __name__ == '__main__':
    # VULNERABILITY: Debug mode exposed on all interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
