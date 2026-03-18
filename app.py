"""
Vulnerable AI Application with intentional security flaws
DO NOT USE IN PRODUCTION - For security scanning demonstration only
"""

from flask import Flask, request, jsonify, render_template_string
import os
import subprocess
import sqlite3

# Import our vulnerable modules
import config
from model_loader import InsecureModelLoader, load_untrusted_model

# Vulnerable AI library imports
import openai
from transformers import pipeline
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI as LangChainOpenAI

app = Flask(__name__)

# VULNERABILITY: Hardcoded secret key
app.secret_key = "super-secret-key-123"  # EXPOSED SECRET

# VULNERABILITY: Debug mode enabled in production
app.config['DEBUG'] = True
app.config['ENV'] = 'production'  # Debug + production = DANGEROUS!

# VULNERABILITY: Setting API keys from config (hardcoded secrets)
openai.api_key = config.OPENAI_API_KEY  # EXPOSED SECRET
os.environ['OPENAI_API_KEY'] = config.OPENAI_API_KEY
os.environ['HUGGINGFACE_TOKEN'] = config.HUGGINGFACE_TOKEN

# Initialize insecure model loader
model_loader = InsecureModelLoader()

# VULNERABILITY: SQL injection - direct string formatting
def get_user_data(username):
    """
    CRITICAL VULNERABILITY: SQL Injection
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABLE: Direct string formatting in SQL query
    query = f"SELECT * FROM users WHERE username = '{username}'"  # SQL INJECTION!
    cursor.execute(query)
    
    return cursor.fetchall()


@app.route('/')
def index():
    """
    VULNERABILITY: Template injection via render_template_string
    """
    user_input = request.args.get('name', 'World')
    
    # VULNERABLE: Direct template rendering with user input
    template = f"<h1>Hello {user_input}!</h1>"  # Template injection!
    return render_template_string(template)


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    CRITICAL VULNERABILITY: Prompt injection and no input sanitization
    """
    data = request.json
    user_prompt = data.get('prompt', '')
    
    # VULNERABLE: No prompt sanitization or validation
    # User can inject malicious prompts to manipulate the AI
    llm = LangChainOpenAI(
        temperature=0.7,
        openai_api_key=config.OPENAI_API_KEY  # EXPOSED SECRET
    )
    
    # VULNERABLE: Direct user input to LLM without filtering
    prompt_template = PromptTemplate(
        input_variables=["user_input"],
        template="User says: {user_input}\nAI responds:"  # No safety guardrails!
    )
    
    chain = LLMChain(llm=llm, prompt=prompt_template)
    
    # VULNERABLE: No output filtering
    response = chain.run(user_input=user_prompt)
    
    # VULNERABLE: Using eval() on AI output
    if "execute:" in response:
        code = response.split("execute:")[1]
        result = eval(code)  # EXTREMELY DANGEROUS!
        return jsonify({"response": response, "execution_result": result})
    
    return jsonify({"response": response})


@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """
    VULNERABILITY: Using vulnerable transformers version
    """
    text = request.json.get('text', '')
    
    # VULNERABLE: Using old transformers library with known CVEs
    classifier = pipeline("sentiment-analysis")
    
    # VULNERABLE: No input length validation (DoS risk)
    result = classifier(text)
    
    return jsonify(result)


@app.route('/api/load-model', methods=['POST'])
def load_model():
    """
    CRITICAL VULNERABILITY: Loading untrusted models
    """
    model_path = request.json.get('model_path', '')
    
    # VULNERABLE: Loading model from user-provided path
    # Allows directory traversal and arbitrary file reading
    model = load_untrusted_model(model_path)  # EXTREMELY DANGEROUS!
    
    return jsonify({"status": "Model loaded", "path": model_path})


@app.route('/api/download-model', methods=['POST'])
def download_model():
    """
    CRITICAL VULNERABILITY: Downloading models from untrusted URLs
    """
    url = request.json.get('url', '')
    
    # VULNERABLE: No URL validation, downloads from any source
    model = model_loader.load_model_from_url(url)  # DANGEROUS!
    
    return jsonify({"status": "Model downloaded"})


@app.route('/api/execute', methods=['POST'])
def execute_command():
    """
    CRITICAL VULNERABILITY: Command injection
    """
    command = request.json.get('command', '')
    
    # VULNERABLE: Executing user-provided commands
    result = os.system(command)  # COMMAND INJECTION!
    
    return jsonify({"result": result})


@app.route('/api/process', methods=['POST'])
def process_data():
    """
    VULNERABILITY: Using subprocess with shell=True
    """
    filename = request.json.get('filename', '')
    
    # VULNERABLE: Command injection via subprocess
    cmd = f"cat {filename}"  # No input sanitization
    output = subprocess.check_output(cmd, shell=True)  # DANGEROUS!
    
    return jsonify({"output": output.decode()})


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    CRITICAL VULNERABILITY: Exposing configuration including secrets
    """
    # VULNERABLE: Returning all config including API keys
    return jsonify({
        "openai_key": config.OPENAI_API_KEY,  # EXPOSED!
        "aws_key": config.AWS_ACCESS_KEY_ID,  # EXPOSED!
        "aws_secret": config.AWS_SECRET_ACCESS_KEY,  # EXPOSED!
        "database_url": config.DATABASE_URL,  # EXPOSED!
        "jwt_secret": config.JWT_SECRET_KEY  # EXPOSED!
    })


@app.route('/api/search', methods=['GET'])
def search_users():
    """
    CRITICAL VULNERABILITY: SQL injection via query parameter
    """
    search_term = request.args.get('q', '')
    
    # VULNERABLE: SQL injection
    users = get_user_data(search_term)  # SQL INJECTION!
    
    return jsonify({"users": users})


@app.route('/api/eval', methods=['POST'])
def eval_code():
    """
    CRITICAL VULNERABILITY: Arbitrary code execution via eval()
    """
    code = request.json.get('code', '')
    
    # VULNERABLE: Executing arbitrary Python code
    result = eval(code)  # EXTREMELY DANGEROUS!
    
    return jsonify({"result": str(result)})


@app.route('/api/upload-model', methods=['POST'])
def upload_model():
    """
    CRITICAL VULNERABILITY: Unsafe file upload and deserialization
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    
    # VULNERABLE: No file type validation
    # VULNERABLE: No size limit
    # VULNERABLE: Saving to predictable location
    filepath = f"/tmp/{file.filename}"  # Path traversal possible!
    file.save(filepath)
    
    # VULNERABLE: Directly loading uploaded pickle file
    model = model_loader.load_pickle_model(filepath)  # DANGEROUS!
    
    return jsonify({"status": "Model uploaded and loaded"})


@app.route('/api/yaml-config', methods=['POST'])
def load_yaml():
    """
    CRITICAL VULNERABILITY: Unsafe YAML deserialization
    """
    yaml_content = request.json.get('yaml', '')
    
    # VULNERABLE: Using unsafe YAML loading
    config_data = model_loader.load_yaml_config(yaml_content)
    
    return jsonify({"config": config_data})


@app.route('/debug/env', methods=['GET'])
def debug_env():
    """
    CRITICAL VULNERABILITY: Exposing environment variables
    """
    # VULNERABLE: Returning all environment variables including secrets
    return jsonify(dict(os.environ))  # EXPOSES ALL SECRETS!


@app.route('/api/ai-completion', methods=['POST'])
def ai_completion():
    """
    VULNERABILITY: Direct OpenAI API call with no rate limiting or filtering
    """
    prompt = request.json.get('prompt', '')
    
    # VULNERABLE: No rate limiting
    # VULNERABLE: No prompt filtering
    # VULNERABLE: No output filtering
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,  # Direct user input!
        max_tokens=2000,  # No cost control
        api_key=config.OPENAI_API_KEY  # EXPOSED SECRET
    )
    
    return jsonify(response)


# VULNERABILITY: Exposing internal paths and structure
@app.errorhandler(500)
def internal_error(error):
    """
    VULNERABILITY: Detailed error messages with stack traces
    """
    import traceback
    return jsonify({
        "error": str(error),
        "traceback": traceback.format_exc(),  # EXPOSES INTERNAL DETAILS!
        "config": {
            "debug": app.config['DEBUG'],
            "secret_key": app.secret_key  # EXPOSED!
        }
    }), 500


if __name__ == '__main__':
    # VULNERABLE: Running with debug=True and publicly accessible
    # VULNERABLE: No authentication required
    # VULNERABLE: Listening on all interfaces
    app.run(
        host='0.0.0.0',  # Accessible from anywhere!
        port=5000,
        debug=True,  # Debug mode in production!
        threaded=True
    )
    
    print(f"[INSECURE] Server running with DEBUG=True")
    print(f"[INSECURE] API Key: {config.OPENAI_API_KEY}")  # Logging secrets!
