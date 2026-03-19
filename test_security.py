"""
Test file with security vulnerabilities for Claude Code to detect
"""
import pickle
import subprocess
import os
import yaml

# SECURITY ISSUE 1: Hardcoded credentials
API_KEY = "sk-test-1234567890abcdef"
DATABASE_PASSWORD = "admin123"
SECRET_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

class DataHandler:
    def __init__(self):
        # SECURITY ISSUE 2: Hardcoded database connection
        self.db_connection = "postgresql://admin:password123@localhost:5432/mydb"
    
    def load_data(self, filename):
        """SECURITY ISSUE 3: Insecure deserialization with pickle"""
        with open(filename, 'rb') as f:
            return pickle.load(f)  # CWE-502: Deserialization of Untrusted Data
    
    def load_config(self, config_file):
        """SECURITY ISSUE 4: Unsafe YAML loading"""
        with open(config_file, 'r') as f:
            return yaml.load(f)  # Should use yaml.safe_load()
    
    def execute_command(self, user_input):
        """SECURITY ISSUE 5: Command injection vulnerability"""
        # Using os.system with user input
        os.system(f"ls {user_input}")
        
        # Using subprocess with shell=True
        subprocess.call(f"grep {user_input} /var/log/app.log", shell=True)
        
        # Another command injection
        subprocess.run(user_input, shell=True, capture_output=True)
    
    def query_database(self, user_id):
        """SECURITY ISSUE 6: SQL injection vulnerability"""
        query = f"SELECT * FROM users WHERE id = {user_id}"
        return query
    
    def search_users(self, search_term):
        """SECURITY ISSUE 7: More SQL injection"""
        sql = "SELECT * FROM users WHERE name = '" + search_term + "'"
        return sql
    
    def eval_code(self, user_code):
        """SECURITY ISSUE 8: Arbitrary code execution"""
        return eval(user_code)
    
    def exec_code(self, code):
        """SECURITY ISSUE 9: Dynamic code execution"""
        exec(code)

def weak_crypto():
    """SECURITY ISSUE 10: Weak cryptographic practices"""
    import hashlib
    
    # Using MD5 (weak hash)
    password = "password123"
    hash_md5 = hashlib.md5(password.encode()).hexdigest()
    
    # Using SHA1 (also weak)
    hash_sha1 = hashlib.sha1(password.encode()).hexdigest()
    
    return hash_md5, hash_sha1

def insecure_random():
    """SECURITY ISSUE 11: Insecure random number generation"""
    import random
    
    # Using random for security-sensitive operations
    session_token = random.randint(1000, 9999)
    return session_token

# SECURITY ISSUE 12: Debug mode enabled
DEBUG = True
if DEBUG:
    import pdb
    pdb.set_trace()

# SECURITY ISSUE 13: Exposed sensitive information
print(f"API Key: {API_KEY}")
print(f"Database Password: {DATABASE_PASSWORD}")
