# Intentionally vulnerable Dockerfile for security scanning demo
# DO NOT USE IN PRODUCTION

# VULNERABILITY: Using older Python base image
FROM python:3.9-slim

# VULNERABILITY: Running as root (no USER directive)
# VULNERABILITY: Exposing secrets in environment variables
ENV OPENAI_API_KEY="sk-proj-AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEfGhIjKlMnOpQrStUvWxYz"
ENV AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
ENV AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
ENV DATABASE_PASSWORD="SuperSecretPassword123!"

# VULNERABILITY: No metadata labels
# VULNERABILITY: Installing as root
WORKDIR /app

# VULNERABILITY: COPY . . includes secrets and sensitive files
COPY . .

# VULNERABILITY: pip install without version pinning for system packages
# VULNERABILITY: No pip cache cleanup
RUN apt-get update && \
    apt-get install -y \
    gcc \
    g++ \
    wget \
    curl \
    git \
    vim \
    net-tools \
    telnet \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

# VULNERABILITY: Exposing internal port without documentation
EXPOSE 5000

# VULNERABILITY: No health check defined
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#   CMD curl -f http://localhost:5000/ || exit 1

# VULNERABILITY: Running application as root
# VULNERABILITY: Debug mode enabled
# VULNERABILITY: No signal handling
CMD ["python", "app.py"]

# Additional vulnerabilities demonstrated:
# - No .dockerignore file (copies unnecessary files)
# - No multi-stage build (larger image, more attack surface)
# - Installing dev tools in production image
# - No image scanning in build process
# - Hardcoded credentials in ENV
# - Running on port 5000 (common default, easily scannable)
# - No resource limits (CPU/memory)
# - No read-only root filesystem
# - Unnecessary packages installed (telnet, vim, etc.)
