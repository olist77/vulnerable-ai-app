# TMAS Docker Image Scanning Guide - AWS ECR

## Image Information
- **Repository URI**: `780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app`
- **Tags**: `latest`, `v1.0`
- **AWS Account**: `780477232234`
- **Region**: `us-east-1`

## Prerequisites
1. TMAS CLI installed (v2.208.0 or later)
2. AWS CLI configured with proper credentials
3. Trend Vision One API key set as environment variable

## Scanning the ECR Image

### Step 1: Authenticate Docker to ECR
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 780477232234.dkr.ecr.us-east-1.amazonaws.com
```

### Step 2: Run TMAS Scan on the ECR Image

#### Basic Scan
```bash
tmas scan --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest
```

#### Scan with SBOM Output
```bash
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest \
  --sbom \
  --output sbom-ecr.json
```

#### Scan with Full Reporting
```bash
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest \
  --sbom \
  --output sbom-ecr.json \
  --malwareScan \
  --saveSBOM
```

#### Scan with Policy Enforcement
```bash
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest \
  --policy-path .tmas/policy.json \
  --fail-on-violation
```

### Step 3: Alternative - Scan Without Docker Pull

If you want to scan the image directly from ECR without pulling:

```bash
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest \
  --region us-east-1 \
  --platform linux/amd64
```

## Expected Vulnerabilities in This Image

This intentionally vulnerable demo should detect:

### 1. **Python Package Vulnerabilities**
- `transformers==4.28.0` - Multiple CVEs including:
  - CVE-2023-4863 (High severity)
  - Arbitrary code execution risks
- `torch==2.0.0` - Known vulnerabilities
- `protobuf==3.19.0` - Multiple CVEs
- `Pillow==9.0.0` - Critical image processing vulnerabilities
- `numpy==1.21.0` - Security issues
- `requests==2.27.1` - Known vulnerabilities

### 2. **Base Image Vulnerabilities**
- `python:3.9-slim` base image contains outdated system packages

### 3. **Malware Scanning**
- Test patterns in malicious model files
- Suspicious Python code patterns

### 4. **Secrets Detection**
- Hardcoded API keys in Dockerfile environment variables:
  - `OPENAI_API_KEY`
  - `AWS_ACCESS_KEY_ID`
  - `AWS_SECRET_ACCESS_KEY`
  - `DATABASE_PASSWORD`

### 5. **SBOM/AISBOM Analysis**
- Complete software bill of materials
- AI model dependencies
- License compliance issues

## Detailed Scan Options

### Generate Comprehensive Report
```bash
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest \
  --sbom \
  --output-format json \
  --output full-report.json \
  --malwareScan \
  --saveSBOM \
  --verbose
```

### Scan Specific Tag (v1.0)
```bash
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:v1.0 \
  --sbom \
  --output sbom-v1.0.json
```

### CI/CD Integration Example
```bash
#!/bin/bash
set -e

# Authenticate to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  780477232234.dkr.ecr.us-east-1.amazonaws.com

# Run TMAS scan
tmas scan \
  --image 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest \
  --sbom \
  --output sbom-report.json \
  --malwareScan \
  --fail-on-violation || {
    echo "Security scan failed - critical vulnerabilities detected"
    exit 1
  }

echo "Security scan passed"
```

## Understanding the Results

### Vulnerability Severity Levels
- **CRITICAL**: Immediate action required - exploitable vulnerabilities
- **HIGH**: Should be fixed soon - significant security risk
- **MEDIUM**: Plan to fix - moderate security risk
- **LOW**: Fix when convenient - minimal security risk

### SBOM Components
The SBOM will include:
- Python packages and versions
- System libraries
- AI/ML models and their metadata
- Dependencies and transitive dependencies

### Recommended Actions
1. **Review Critical & High vulnerabilities first**
2. **Update vulnerable packages**:
   ```
   transformers>=4.38.0
   torch>=2.1.0
   protobuf>=4.21.0
   Pillow>=10.0.0
   numpy>=1.24.0
   requests>=2.31.0
   ```
3. **Remove hardcoded secrets from Dockerfile**
4. **Update base image** to `python:3.11-slim` or later
5. **Re-scan after fixes** to verify remediation

## Additional Resources

- [TMAS Documentation](https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-tmas-examples)
- [Scanning OCI Images](https://docs.trendmicro.com/en-us/documentation/article/trend-vision-one-tmas-examples#GUID-F8FAF1DF-7A1E-4C0A-ADA3-6F6FC6CAD49D-atz560)
- [AWS ECR Best Practices](https://docs.aws.amazon.com/AmazonECR/latest/userguide/security-best-practices.html)

## Quick Command Reference

```bash
# List images in ECR
aws ecr list-images --repository-name vulnerable-ai-app --region us-east-1

# Get image digest
aws ecr describe-images --repository-name vulnerable-ai-app \
  --region us-east-1 --image-ids imageTag=latest

# Pull image locally (if needed)
docker pull 780477232234.dkr.ecr.us-east-1.amazonaws.com/vulnerable-ai-app:latest

# Scan local image
docker images
tmas scan --image vulnerable-ai-app:latest
```

---

**Note**: This is an intentionally vulnerable demo application for testing security scanning tools. DO NOT deploy to production!
