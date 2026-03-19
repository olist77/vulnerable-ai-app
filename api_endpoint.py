"""
API endpoint with security vulnerabilities for Claude to review
"""
from flask import Flask, request, jsonify
import sqlite3
import subprocess
import os

app = Flask(__name__)

# Hardcoded database credentials
DB_USER = "admin"
DB_PASS = "SuperSecret123"
API_SECRET = "sk-1234567890"

@app.route('/api/user/<user_id>')
def get_user(user_id):
    """SQL Injection vulnerability"""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # Vulnerable: direct string interpolation
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return jsonify(cursor.fetchall())

@app.route('/api/search')
def search():
    """Another SQL injection"""
    search_term = request.args.get('q')
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE name LIKE '%" + search_term + "%'"
    return jsonify(conn.execute(query).fetchall())

@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a@a  # Dangerous: executing user input
    result = os.system(cmd)
    return    return    return    return    reoute('/api/ping')
defdefdefdefdefdefdAnother commadefdefdefdefdefdefdAhosdefdefdefdefdefdefdAnother comm.8defdefdefdefdefdng shell=True is dangerous
    output = subprocess.check_ou    output = subprocess.check_ouTr    output = subprout

if __name__ == '__main__':
    # Debug    # Debug    # Debug    # Debuisk
                      , host='0.0.0.0')
