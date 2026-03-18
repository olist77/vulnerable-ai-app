"""
Insecure model loading module with pickle deserialization vulnerabilities
DO NOT USE IN PRODUCTION - Demonstrates dangerous patterns for security testing
"""

import pickle
import yaml
import os
import requests
from io import BytesIO

# Insecure imports that enable dangerous operations
import dill  # Can execute arbitrary code during deserialization
import joblib
import marshal

from config import MODEL_STORAGE_URL, AWS_ACCESS_KEY_ID


class InsecureModelLoader:
    """
    VULNERABILITY: This class demonstrates multiple insecure deserialization patterns
    """
    
    def __init__(self):
        self.models_cache = {}
    
    def load_pickle_model(self, model_path):
        """
        CRITICAL VULNERABILITY: Unsafe pickle deserialization
        CVE-2023-xxxxx equivalent - Arbitrary code execution
        
        pickle.load() can execute arbitrary Python code during deserialization.
        An attacker can craft a malicious pickle file to execute commands.
        """
        print(f"[INSECURE] Loading model from pickle: {model_path}")
        
        # VULNERABLE: No validation or sandboxing
        with open(model_path, 'rb') as f:
            model = pickle.load(f)  # DANGEROUS!
        
        return model
    
    def load_model_from_url(self, url):
        """
        CRITICAL VULNERABILITY: Downloading and deserializing untrusted data
        Combines multiple vulnerabilities:
        1. HTTP instead of HTTPS (man-in-the-middle attack)
        2. No URL validation
        3. Unsafe deserialization
        """
        print(f"[INSECURE] Downloading model from: {url}")
        
        # VULNERABLE: Using HTTP, no SSL verification
        response = requests.get(url, verify=False)  # SSL verification disabled!
        
        # VULNERABLE: Directly deserializing downloaded content
        model = pickle.loads(response.content)  # EXTREMELY DANGEROUS!
        
        return model
    
    def load_yaml_config(self, config_path):
        """
        CRITICAL VULNERABILITY: Unsafe YAML deserialization
        CVE-2020-14343 equivalent - Arbitrary code execution
        
        yaml.load() without Loader parameter uses FullLoader which can
        instantiate arbitrary Python objects
        """
        print(f"[INSECURE] Loading YAML config: {config_path}")
        
        with open(config_path, 'r') as f:
            # VULNERABLE: Using unsafe yaml.load()
            config = yaml.load(f)  # DANGEROUS! Should use yaml.safe_load()
        
        return config
    
    def load_with_eval(self, model_config_str):
        """
        CRITICAL VULNERABILITY: Using eval() on untrusted input
        Allows arbitrary code execution
        """
        print(f"[INSECURE] Evaluating model config with eval()")
        
        # VULNERABLE: eval() executes arbitrary Python code
        config = eval(model_config_str)  # EXTREMELY DANGEROUS!
        
        return config
    
    def load_with_exec(self, model_code):
        """
        CRITICAL VULNERABILITY: Using exec() on untrusted input
        Allows arbitrary code execution
        """
        print(f"[INSECURE] Executing model initialization code with exec()")
        
        # VULNERABLE: exec() executes arbitrary Python code
        exec(model_code)  # EXTREMELY DANGEROUS!
    
    def load_dill_model(self, model_path):
        """
        VULNERABILITY: Dill deserialization is even more dangerous than pickle
        Can serialize and deserialize more Python objects including lambdas
        """
        print(f"[INSECURE] Loading dill model: {model_path}")
        
        with open(model_path, 'rb') as f:
            # VULNERABLE: Dill is more powerful and dangerous than pickle
            model = dill.load(f)  # DANGEROUS!
        
        return model
    
    def load_joblib_model(self, model_path):
        """
        VULNERABILITY: Joblib also uses pickle under the hood
        """
        print(f"[INSECURE] Loading joblib model: {model_path}")
        
        # VULNERABLE: joblib.load uses pickle internally
        model = joblib.load(model_path)  # DANGEROUS!
        
        return model
    
    def load_marshal_data(self, data_path):
        """
        VULNERABILITY: Marshal can deserialize and execute code objects
        """
        print(f"[INSECURE] Loading marshal data: {data_path}")
        
        with open(data_path, 'rb') as f:
            # VULNERABLE: Can load compiled code objects
            data = marshal.load(f)  # DANGEROUS!
        
        return data
    
    def download_model_no_verify(self, url, save_path):
        """
        VULNERABILITY: Downloads files over HTTP without verification
        Susceptible to man-in-the-middle attacks
        """
        print(f"[INSECURE] Downloading model without SSL verification")
        
        # VULNERABLE: No SSL/TLS verification
        response = requests.get(
            url,
            verify=False,  # DANGEROUS! Disables certificate verification
            timeout=None  # DANGEROUS! No timeout
        )
        
        # VULNERABLE: No file type validation
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        # VULNERABLE: Directly loading the downloaded file
        return self.load_pickle_model(save_path)
    
    def load_model_with_system_call(self, model_name):
        """
        CRITICAL VULNERABILITY: Command injection via os.system()
        """
        print(f"[INSECURE] Loading model via system call")
        
        # VULNERABLE: Command injection - no input sanitization
        command = f"cat models/{model_name}.pkl"
        os.system(command)  # DANGEROUS! Command injection vulnerability


def load_untrusted_model(user_provided_path):
    """
    CRITICAL VULNERABILITY: Loading models from user-provided paths
    No validation of file path or contents
    """
    # VULNERABLE: No path validation, directory traversal possible
    # User could provide "../../../etc/passwd" or similar
    
    with open(user_provided_path, 'rb') as f:
        # VULNERABLE: Blindly deserializing user-provided file
        model = pickle.load(f)
    
    return model


def create_malicious_model_example():
    """
    Example of how an attacker could create a malicious pickle file
    This demonstrates why pickle deserialization is dangerous
    """
    import pickle
    import os
    
    class MaliciousPayload:
        def __reduce__(self):
            # This will execute when unpickled
            cmd = 'echo "Malicious code executed!" > /tmp/hacked.txt'
            return (os.system, (cmd,))
    
    # Serializing this object creates a malicious pickle file
    payload = MaliciousPayload()
    with open('malicious_model.pkl', 'wb') as f:
        pickle.dump(payload, f)
    
    print("[WARNING] Created malicious_model.pkl - DO NOT DISTRIBUTE")


# Example vulnerable usage patterns
if __name__ == "__main__":
    loader = InsecureModelLoader()
    
    # Demonstrating various vulnerability patterns
    print("\n=== DEMONSTRATING INSECURE PATTERNS ===\n")
    
    # Pattern 1: Loading from untrusted source
    print("1. Loading model from HTTP URL (INSECURE)")
    # model = loader.load_model_from_url("http://untrusted-site.com/model.pkl")
    
    # Pattern 2: Using eval on user input
    print("\n2. Using eval() on user input (INSECURE)")
    user_input = "{'model_type': 'transformer'}"  # In reality, could be malicious
    # config = loader.load_with_eval(user_input)
    
    # Pattern 3: Loading YAML without safe_load
    print("\n3. Using unsafe YAML loading (INSECURE)")
    # config = loader.load_yaml_config("model_config.yaml")
    
    # Pattern 4: Command injection
    print("\n4. Command injection via os.system (INSECURE)")
    # loader.load_model_with_system_call("transformer_model")
    
    print("\n=== ALL PATTERNS ABOVE ARE VULNERABLE ===")
    print("These should be detected by security scanners!")
