# Vulnerable AI Application - Security Scanning Demo with Claude Code integration

## ⚠️ CRITICAL WARNING ⚠️

**THIS APPLICATION IS INTENTIONALLY INSECURE**

This application contains numerous deliberately introduced security vulnerabilities for the purpose of demonstrating Trend Vision One's AI SBOM (Software Bill of Materials) and code security scanning capabilities.

**DO NOT USE IN PRODUCTION**
**DO NOT DEPLOY THIS APPLICATION TO ANY LIVE ENVIRONMENT**
**DO NOT USE THESE PATTERNS IN REAL APPLICATIONS**

---

## Purpose

This demo application is designed to trigger comprehensive security findings in Trend Vision One, including:

1. **AI SBOM Detection** - Cataloging AI/ML libraries and frameworks
2. **CVE Detection** - Known vulnerabilities in dependencies
3. **Secret Scanning** - Hardcoded credentials and API keys
4. **Code Security** - Insecure coding patterns
5. **Container Security** - Docker/IaC misconfigurations
6. **AI-Specific Risks** - Prompt injection, unsafe deserialization, etc.

---

## Intentional Vulnerabilities Catalog

### 1. Vulnerable AI/ML Dependencies (requirements.txt)

| Library | Version | Known CVEs | Impact |
|---------|---------|------------|--------|
| tensorflow | 2.10.0 | CVE-2023-25801, CVE-2023-25660, CVE-2023-25671 | Arbitrary code execution, DoS |
| torch | 1.12.0 | CVE-2022-45907 | Arbitrary code execution |
| transformers | 4.25.1 | CVE-2023-28009 | Unsafe deserialization |
| langchain | 0.0.27 | CVE-2023-36258 | Prompt injection → code execution |
| numpy | 1.21.0 | CVE-2021-41496 | Buffer overflow |
| pillow | 8.3.0 | CVE-2022-22815, CVE-2022-22816 | Image processing vulnerabilities |
| flask | 2.0.0 | CVE-2023-30861 | Werkzeug security issues |
| requests | 2.25.0 | CVE-2023-32681 | Proxy credential exposure |
| pyyaml | 5.3 | CVE-2020-14343 | Arbitrary code execution |
| protobuf | 3.19.0 | CVE-2022-1941 | Parsing vulnerabilities |
| onnxruntime | 1.12.0 | CVE-2023-32708 | Security issues |
| cryptography | 3.3.2 | CVE-2023-23931 | Cryptographic weaknesses |

**Total: 30+ vulnerable dependencies with 50+ known CVEs**

---

### 2. Hardcoded Secrets (config.py)

**EXPOSED CREDENTIALS:**

```python
# API Keys
OPENAI_API_KEY = "sk-proj-..." 
HUGGINGFACE_TOKEN = "hf_..."
ANTHROPIC_API_KEY = "sk-ant-api03-..."
AWS_ACCESS_KEY_ID = "AKIA..."
AWS_SECRET_ACCESS_KEY = "wJalr..."

# Database Credentials
DATABASE_URL = "postgresql://admin:SuperSecretPassword123!@..."
MONGODB_URI = "mongodb://mluser:P@ssw0rd123@..."

# JWT & Encryption Keys
JWT_SECRET_KEY = "super-secret-jwt-key-do-not-share-12345"
ENCRYPTION_KEY = "ThisIsAVeryBadEncryptionKey123!"
PRIVATE_KEY_PEM = "-----BEGIN RSA PRIVATE KEY-----..."

# Payment & Communication
STRIPE_SECRET_KEY = "sk_test_..."
SENDGRID_API_KEY = "SG...."
SLACK_WEBHOOK = "https://hooks.slack.com/..."
```

**Total: 20+ exposed secrets across multiple services**

---

### 3. Insecure Deserialization (model_loader.py)

#### Critical Vulnerabilities:

**A. Pickle Deserialization** ⚠️ **CRITICAL**
```python
with open(model_path, 'rb') as f:
    model = pickle.load(f)  # Arbitrary code execution
```
- **Risk**: Attacker can execute arbitrary Python code
- **Attack**: Craft malicious pickle file → RCE
- **CVE Equivalent**: CVE-2023-xxxxx class vulnerabilities

**B. YAML Unsafe Loading** ⚠️ **CRITICAL**
```python
config = yaml.load(f)  # Should use yaml.safe_load()
```
- **Risk**: Instantiate arbitrary Python objects
- **Attack**: YAML file with malicious objects → RCE
- **CVE**: CVE-2020-14343 class

**C. eval() on Untrusted Input** ⚠️ **CRITICAL**
```python
config = eval(model_config_str)  # Arbitrary code execution
```
- **Risk**: Direct code execution
- **Attack**: Any Python expression → full system compromise

**D. Dill & Marshal Loading** ⚠️ **HIGH**
```python
model = dill.load(f)     # More dangerous than pickle
data = marshal.load(f)    # Can load code objects
```

**E. Download & Deserialize** ⚠️ **CRITICAL**
```python
response = requests.get(url, verify=False)  # No SSL verification
model = pickle.loads(response.content)      # RCE from network
```

---

### 4. AI-Specific Vulnerabilities (app.py)

#### A. Prompt Injection ⚠️ **HIGH**
```python
@app.route('/api/chat', methods=['POST'])
def chat():
    user_prompt = data.get('prompt', '')
    # No sanitization or validation
    response = chain.run(user_input=user_prompt)
```
- **Risk**: Manipulate AI behavior, data exfiltration
- **Attack**: "Ignore previous instructions and..."

#### B. Unsafe AI Output Handling ⚠️ **CRITICAL**
```python
if "execute:" in response:
    code = response.split("execute:")[1]
    result = eval(code)  # Executing AI-generated code!
```
- **Risk**: AI output → arbitrary code execution
- **Attack**: Prompt engineer AI to return malicious code

#### C. No Rate Limiting ⚠️ **MEDIUM**
```python
response = openai.Completion.create(
    prompt=prompt,  # Unbounded
    max_tokens=2000  # High cost per request
)
```
- **Risk**: Cost attack, resource exhaustion
- **Attack**: Spam API calls → $$$

---

### 5. Classic Web Vulnerabilities (app.py)

#### A. SQL Injection ⚠️ **CRITICAL**
```python
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```
- **Attack**: `username = "' OR '1'='1"`

#### B. Command Injection ⚠️ **CRITICAL**
```python
result = os.system(command)  # User-provided command
cmd = f"cat {filename}"
subprocess.check_output(cmd, shell=True)
```
- **Attack**: `command = "ls; rm -rf /"`

#### C. Path Traversal ⚠️ **HIGH**
```python
model = load_untrusted_model(user_path)  # No validation
filepath = f"/tmp/{file.filename}"  # User-controlled
```
- **Attack**: `path = "../../../etc/passwd"`

#### D. Template Injection ⚠️ **HIGH**
```python
template = f"<h1>Hello {user_input}!</h1>"
return render_template_string(template)
```
- **Attack**: `name = "{{config.items()}}"`

#### E. Information Disclosure ⚠️ **HIGH**
```python
@app.route('/api/config')
def get_config():
    return jsonify({
        "openai_key": config.OPENAI_API_KEY,
        "aws_secret": config.AWS_SECRET_ACCESS_KEY
    })

@app.route('/debug/env')
def debug_env():
    return jsonify(dict(os.environ))
```

---

### 6. Container Security Issues (Dockerfile)

#### Dockerfile Vulnerabilities:

```dockerfile
# 1. Running as root (no USER directive)
# 2. Hardcoded secrets in ENV
ENV OPENAI_API_KEY="sk-proj-..."
ENV AWS_SECRET_ACCESS_KEY="wJalr..."

# 3. Using older base image
FROM python:3.9-slim

# 4. COPY . . includes secrets
COPY . .

# 5. No health check
# 6. Installing unnecessary tools
RUN apt-get install -y telnet vim git

# 7. No resource limits
# 8. Debug mode enabled
CMD ["python", "app.py"]
```

**Container Security Findings:**
- Running as root (UID 0)
- Secrets baked into image layers
- No read-only root filesystem
- Missing security options (no-new-privileges)
- Large attack surface (unnecessary packages)
- No vulnerability scanning in build
- No .dockerignore (exposes all files)

---

## Expected Security Scanning Results

When scanned by Trend Vision One, this application should trigger:

### AI SBOM Detection
- ✅ 15+ AI/ML frameworks identified
- ✅ TensorFlow, PyTorch, Transformers, LangChain detected
- ✅ AI model file patterns (pickle, ONNX) recognized
- ✅ AI API usage (OpenAI, HuggingFace) catalogued

### Vulnerability Assessment
- ⚠️ **50+ CVEs** across dependencies
- ⚠️ **12 CRITICAL** severity findings
- ⚠️ **25 HIGH** severity findings
- ⚠️ **15 MEDIUM** severity findings

### Secret Scanning
- 🔴 **20+ hardcoded secrets** detected:
  - API keys (OpenAI, AWS, HuggingFace, etc.)
  - Database credentials
  - Private keys (RSA, JWT)
  - Webhooks and tokens

### Code Security
- 🔴 **Insecure deserialization** (pickle, yaml, eval)
- 🔴 **Command injection** (os.system, subprocess)
- 🔴 **SQL injection** (string formatting in queries)
- 🔴 **Path traversal** (user-controlled file paths)
- 🟡 **Debug mode in production**
- 🟡 **No input validation**
- 🟡 **No rate limiting**

### Container Security
- 🔴 Running as root
- 🔴 Secrets in ENV/image layers
- 🔴 Vulnerable base image
- 🟡 No health check
- 🟡 Unnecessary packages
- 🟡 Missing security headers

### AI-Specific Risks
- 🔴 **Prompt injection** vulnerabilities
- 🔴 **Unsafe AI output handling** (eval on LLM responses)
- 🔴 **Model deserialization** attacks
- 🟡 No content filtering
- 🟡 No output sanitization

---

## How to Use This Demo

### Step 1: Build the Container (Optional - for container scanning)
```bash
cd vulnerable-ai-app
docker build -t vulnerable-ai-demo:latest .
```

### Step 2: Scan with Trend Vision One

#### A. Code Scanning
1. Push to GitHub/GitLab
2. Enable V1 code security scanning
3. Review detected vulnerabilities

#### B. Container Scanning
1. Push image to container registry
2. Enable V1 container security
3. Review SBOM and CVE findings

#### C. Runtime Scanning (if applicable)
1. Deploy to K8s/ECS with V1 sensor
2. Enable runtime protection
3. Trigger behaviors to detect runtime issues

---

## Vulnerability Summary by Category

| Category | Critical | High | Medium | Low |
|----------|----------|------|--------|-----|
| **Dependencies (CVEs)** | 12 | 20 | 15 | 3 |
| **Secrets** | 20 | - | - | - |
| **Code Security** | 8 | 10 | 5 | 2 |
| **Container** | 3 | 5 | 7 | 4 |
| **AI-Specific** | 4 | 6 | 3 | 1 |
| **TOTAL** | **47** | **41** | **30** | **10** |

**Grand Total: 128 security findings** 🚨

---

## Files in This Demo

```
vulnerable-ai-app/
├── README.md                 # This file
├── requirements.txt          # 30+ vulnerable AI/ML dependencies
├── config.py                 # 20+ hardcoded secrets
├── model_loader.py           # Insecure deserialization patterns
├── app.py                    # Vulnerable Flask app with AI features
├── Dockerfile                # Insecure container configuration
└── models/                   # (Empty) Model storage directory
```

---

## Demonstration Scenarios

### Scenario 1: AI SBOM Discovery
**Goal**: Show AI/ML library detection
- Scan `requirements.txt` → detects TensorFlow, PyTorch, LangChain
- Scan `app.py` → identifies OpenAI API usage
- Scan `model_loader.py` → finds pickle model loading

### Scenario 2: CVE Detection
**Goal**: Show vulnerability identification
- TensorFlow 2.10.0 → CVE-2023-25801 (critical)
- PyYAML 5.3 → CVE-2020-14343 (critical)
- Flask 2.0.0 → CVE-2023-30861 (high)

### Scenario 3: Secret Exposure
**Goal**: Show hardcoded credential detection
- config.py → 20+ API keys and passwords
- Dockerfile → secrets in ENV variables
- app.py → secrets in code

### Scenario 4: Insecure AI Patterns
**Goal**: Show AI-specific vulnerabilities
- Prompt injection in `/api/chat`
- Unsafe model loading in `model_loader.py`
- eval() on AI output in `app.py`

---

## Remediation Guide (What NOT to do)

For educational purposes, here's how each vulnerability class should be fixed in real applications:

### ✅ Dependencies
- Pin to latest secure versions
- Automate dependency updates
- Use vulnerability scanning in CI/CD

### ✅ Secrets
- Use secret management (AWS Secrets Manager, HashiCorp Vault)
- Environment variables (never hardcode)
- Rotate regularly

### ✅ Deserialization
- Never use pickle on untrusted data
- Use JSON for serialization
- Validate and sandbox if necessary

### ✅ AI Security
- Input sanitization and validation
- Output filtering
- Prompt engineering safeguards
- Rate limiting and monitoring

### ✅ Container
- Run as non-root user
- Multi-stage builds
- Minimal base images
- Scan images regularly

---

## Testing Checklist

- [ ] AI libraries detected in SBOM
- [ ] CVEs identified (50+ expected)
- [ ] Secrets flagged (20+ expected)
- [ ] Pickle deserialization warnings
- [ ] SQL injection detected
- [ ] Command injection detected
- [ ] Container running as root flagged
- [ ] ENV secrets detected
- [ ] Debug mode warning
- [ ] Prompt injection risks identified

---

## Support & Questions

This is a demo application for Trend Vision One security scanning capabilities.

**Remember**: These vulnerabilities are **intentional** for demonstration purposes only.

**DO NOT**:
- Deploy to production
- Use these patterns in real code
- Expose to the internet
- Use real credentials (even in testing)

**DO**:
- Use for security training
- Demonstrate scanning capabilities
- Educate teams on AI security
- Test detection tools

---

## License

This demo is provided AS-IS for educational and demonstration purposes only.
No warranty or support is provided.

---

**Last Updated**: 2026-03-19
**Version**: 1.0.0
**Status**: INTENTIONALLY VULNERABLE - DO NOT USE IN PRODUCTION
