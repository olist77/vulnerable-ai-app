"""
Configuration file with intentionally hardcoded secrets for security scanning demo
DO NOT USE IN PRODUCTION - These are fake credentials for demonstration only
"""

# OpenAI API Keys - EXPOSED SECRET
OPENAI_API_KEY = "sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIjKlMnOpQrStUvWxYz"
OPENAI_ORG_ID = "org-1234567890abcdefghij"

# HuggingFace Tokens - EXPOSED SECRET
HUGGINGFACE_TOKEN = "hf_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"
HUGGINGFACE_API_KEY = "hf_api_AbCdEfGhIjKlMnOpQrStUvWxYz1234567890"

# AWS Credentials - EXPOSED SECRET
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "us-east-1"
AWS_S3_BUCKET = "my-ml-models-bucket"

# Database Credentials - EXPOSED SECRET
DATABASE_URL = "postgresql://admin:SuperSecretPassword123!@ml-db.example.com:5432/production"
MONGODB_URI = "mongodb://mluser:P@ssw0rd123@ml-mongo.example.com:27017/models?authSource=admin"
REDIS_PASSWORD = "RedisP@ssw0rd456!"

# API Keys for various services - EXPOSED SECRETS
ANTHROPIC_API_KEY = "sk-ant-api03-1234567890abcdefghijklmnopqrstuvwxyz"
COHERE_API_KEY = "1234567890abcdefghijklmnopqrstuvwxyz"
REPLICATE_API_TOKEN = "r8_abcdefghij1234567890"
PINECONE_API_KEY = "12345678-1234-1234-1234-123456789012"
PINECONE_ENV = "us-west1-gcp"

# JWT Secret - EXPOSED SECRET
JWT_SECRET_KEY = "super-secret-jwt-key-do-not-share-12345"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 3600

# Encryption Keys - EXPOSED SECRETS
ENCRYPTION_KEY = "ThisIsAVeryBadEncryptionKey123!"
FERNET_KEY = "YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXoxMjM0NTY="

# Private Keys - EXPOSED SECRET (RSA Private Key)
PRIVATE_KEY_PEM = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAy8Dbv8prpJ/0kKhlGeJYozo2t60EG8L0561g13R29LvMR5hy
vGZlGJpmn65+A4xHXInJYiPuKzrKUnApeLZ+vw1HocOAZtWK0z3r26uA8kQYOKX9
Qt/DbCdvsF9wF8gRK0ptx9M6R13NvBxvVQApfc9jB9nTzphOgM4JiEYvlV8FLhg9
yZovMYd6Wwf3aoXK891VQxTr/kQYoq1Yp+68i6T4nNq7NWC+UNVjQHxNQMQMzU6l
WCX8zyg3yH88OAQkUXIXKfQ+NkvYQ1cxaMoVPpY72+eVthKzpMeyHkBn7ciumk5q
gLTEJAfWZpe4f4eFZj/Rc8Y8Jj2IS5kVPjUywQIDAQABAoIBADhg1u1Mv1hAAlX8
omz1Gn2f4AAW2aos2cM5UDCNw1SYmj+9SRIkaxjRsE/C4o9sw1oxrg1/z6kajV0e
N/z7Qj66VJZqeC8J3hPvLN7LGz0qiD8e/pVqQqPJjr3AW96p7K3Fx3g6x6wqcEYQ
7dAl3ks0g0PThWxMdjFBiP7dmqM6KeLBJWqnQzFEKMqFpBHqrPT7qKLz5bLkXGz0
-----END RSA PRIVATE KEY-----"""

# API Endpoints with embedded credentials
INTERNAL_API_URL = "https://admin:P@ssword123@internal-api.example.com/v1"
WEBHOOK_URL = "https://webhook.site/12345678-1234-1234-1234-123456789012?secret=MyWebhookSecret123"

# Slack Webhook - EXPOSED SECRET
SLACK_WEBHOOK = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"

# Model Storage URLs with credentials
MODEL_STORAGE_URL = "ftp://mluser:FtpP@ss123@models.example.com/production/"
MODEL_REGISTRY_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"

# Feature Flags (bad practice: hardcoded)
ENABLE_DEBUG = True
ALLOW_UNSAFE_DESERIALIZATION = True  # Extremely dangerous!
SKIP_INPUT_VALIDATION = True  # Bad practice
DISABLE_RATE_LIMITING = True  # Security risk

# Admin Credentials - EXPOSED SECRET
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Admin123!"
ADMIN_EMAIL = "admin@example.com"

# Third-party service keys
SENDGRID_API_KEY = "SG.1234567890abcdefghijklmnopqrstuvwxyz"
STRIPE_SECRET_KEY = "sk_test_1234567890abcdefghijklmnopqrstuvwxyz"
TWILIO_AUTH_TOKEN = "1234567890abcdefghijklmnopqrstuvwxyz"

# ML Model API Keys
STABILITY_AI_KEY = "sk-1234567890abcdefghijklmnopqrstuvwxyz"
ELEVENLABS_API_KEY = "1234567890abcdefghijklmnopqrstuvwxyz"

# Configuration
APP_SECRET = "flask-secret-key-change-this-in-production"
SESSION_SECRET = "session-secret-12345"
COOKIE_SECRET = "cookie-secret-67890"

# Insecure defaults
ALLOWED_HOSTS = ["*"]  # Allows all hosts - security risk
DEBUG_MODE = True
TESTING = False
ENV = "production"  # Running with debug in production!
