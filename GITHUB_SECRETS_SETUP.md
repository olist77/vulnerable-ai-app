# GitHub Secrets Setup Guide for TMAS Scanning

This guide explains how to configure the required GitHub secrets for the TMAS (Trend Micro Artifact Scanner) GitHub Action.

---

## Required Secrets

### 1. `TMAS_API_KEY` (Required - You must create this)
### 2. `GITHUB_TOKEN` (Automatic - No action needed)

---

## Step-by-Step Setup

### Step 1: Get Your TMAS API Key from Trend Vision One

#### Option A: Using Trend Vision One Console (Recommended)

1. **Log in to Trend Vision One**
   - URL: https://portal.xdr.trendmicro.com/ (or your regional URL)
   - Use your Vision One credentials

2. **Navigate to API Keys**
   - Click on your profile icon (top right)
   - Select **"User Settings"** or **"API Keys"**
   - Or go to: **Administration** → **API Keys**

3. **Create a New API Key**
   - Click **"Add API Key"** or **"Create API Key"**
   - Name: `TMAS GitHub Scanner` (or any descriptive name)
   - Description: `API key for TMAS GitHub Action scanning`
   
4. **Set Permissions**
   Required permissions for TMAS:
   - ✅ **Run artifact scans** (or similar scan permission)
   - ✅ **Read scan results**
   
   The exact permission name may vary:
   - Could be: `Artifact Scanning`
   - Could be: `File Security`
   - Could be: `Code Security`

5. **Select Region**
   - Choose: **us-east-1** (matches the workflow `additionalArgs`)
   - Or your preferred Vision One region

6. **Set Expiration**
   - Recommended: 365 days or custom date
   - For testing: 90 days minimum

7. **Generate and Copy the API Key**
   - Click **"Generate"** or **"Create"**
   - **IMPORTANT**: Copy the API key immediately!
   - Format will look like: `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...` (long JWT token)
   - You won't be able to see it again!

#### Option B: Using Vision One API (Advanced)

If you prefer CLI/API approach:
```bash
# This requires existing V1 API access
curl -X POST https://api.xdr.trendmicro.com/v3.0/iam/apiKeys \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TMAS GitHub Scanner",
    "role": "Artifact Scanner",
    "description": "For GitHub Action TMAS scanning"
  }'
```

---

### Step 2: Add TMAS_API_KEY to GitHub Repository Secrets

1. **Go to Your Repository**
   - URL: https://github.com/olist77/vulnerable-ai-app

2. **Navigate to Settings**
   - Click on **"Settings"** tab (top menu)

3. **Go to Secrets and Variables**
   - In left sidebar, expand **"Secrets and variables"**
   - Click **"Actions"**

4. **Create New Repository Secret**
   - Click **"New repository secret"** button

5. **Add the TMAS API Key**
   - **Name**: `TMAS_API_KEY` (must match exactly)
   - **Value**: Paste the entire API key from Step 1
     ```
     eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlRNQVMgU2Nhbm5lciIsImlhdCI6MTUxNjIzOTAyMn0...
     ```
   - Click **"Add secret"**

6. **Verify Secret is Added**
   - You should see `TMAS_API_KEY` listed under "Repository secrets"
   - The value will be hidden (shows as `***`)

---

### Step 3: Verify GITHUB_TOKEN (Automatic)

The `GITHUB_TOKEN` is **automatically provided** by GitHub Actions and requires **no configuration**.

- ✅ It's automatically available in all workflows
- ✅ Permissions are set automatically by GitHub
- ✅ Used for: Checking out code, posting scan results, creating annotations

**If you need custom permissions** (optional):
```yaml
permissions:
  contents: read        # Read repository contents
  security-events: write # Write security findings
  pull-requests: write   # Comment on PRs with results
```

Add this to the workflow file under the `jobs.tmas-scan` section if needed.

---

## Quick Reference: GitHub UI Path

```
GitHub Repository
└── Settings (tab)
    └── Secrets and variables (left sidebar)
        └── Actions
            └── New repository secret
                ├── Name: TMAS_API_KEY
                └── Value: <your-v1-api-key>
```

---

## Testing the Setup

### Option 1: Push the Workflow File

```bash
cd /Users/stefanoolivieri/Downloads/vulnerable-ai-app

# Add the workflow file
git add .github/workflows/tmas-scan.yml
git add GITHUB_SECRETS_SETUP.md

# Commit
git commit -m "Add TMAS GitHub Action workflow"

# Push to trigger the scan
git push origin main
```

### Option 2: Manual Trigger (if configured)

1. Go to: https://github.com/olist77/vulnerable-ai-app/actions
2. Select "TMAS Scan" workflow
3. Click "Run workflow" button
4. Select branch: `main`
5. Click "Run workflow"

---

## Verify Scan is Running

1. **Go to Actions Tab**
   - https://github.com/olist77/vulnerable-ai-app/actions

2. **Check Workflow Run**
   - You should see "TMAS Scan" workflow running
   - Click on the run to see details

3. **Monitor Progress**
   - "Checkout" step should complete quickly
   - "Download TMAS and Scan Repo" will take 2-5 minutes
   - Scanning 30+ vulnerable dependencies takes time!

4. **View Results**
   - Results will appear in the workflow logs
   - Security findings may appear in: **Security** → **Code scanning alerts**

---

## Expected Scan Results

For this vulnerable-ai-app repository, TMAS should detect:

### Vulnerabilities
- ✅ 50+ CVEs in dependencies
- ✅ TensorFlow 2.10.0 vulnerabilities
- ✅ PyTorch 1.12.0 vulnerabilities
- ✅ Flask, PyYAML, Pillow CVEs
- ✅ Multiple critical and high severity findings

### Secrets
- ✅ 20+ hardcoded secrets detected:
  - OpenAI API keys
  - AWS credentials
  - HuggingFace tokens
  - Database passwords
  - JWT secrets
  - RSA private keys

### Expected Output Summary
```
Scan Results:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Vulnerabilities Found: 50+
  Critical: 12
  High: 25
  Medium: 15
  Low: 3

Secrets Found: 20+
  Critical: 18
  High: 2

Total Issues: 70+
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Troubleshooting

### Issue: "Error: Invalid TMAS API Key"

**Causes:**
- API key not set in GitHub secrets
- Wrong secret name (must be `TMAS_API_KEY` exactly)
- API key expired
- API key lacks required permissions

**Solutions:**
1. Verify secret name is exactly `TMAS_API_KEY`
2. Regenerate API key in Vision One
3. Check API key has "Artifact Scanning" permissions
4. Ensure API key hasn't expired

### Issue: "Error: Authentication failed"

**Causes:**
- API key from wrong Vision One region
- API key permissions insufficient

**Solutions:**
1. Match `--region=us-east-1` with your V1 region
2. Regenerate key with correct permissions
3. Check Vision One console for API key status

### Issue: "Workflow doesn't trigger"

**Causes:**
- Workflow file not in correct location
- Branch not configured in `on.push.branches`

**Solutions:**
1. Ensure file is at: `.github/workflows/tmas-scan.yml`
2. Check branch matches (`main` by default)
3. Manually trigger from Actions tab

### Issue: "Too many secrets detected" (Expected!)

This is **normal** for this demo app! It's intentionally vulnerable.

**Expected behavior:**
- 20+ secrets detected ✅
- Multiple critical findings ✅
- This demonstrates TMAS detection capabilities ✅

---

## Alternative: Using GitHub CLI to Add Secret

If you prefer command line:

```bash
# Make sure you have the TMAS API key
export TMAS_KEY="your-vision-one-api-key-here"

# Add secret to repository
gh secret set TMAS_API_KEY --body "$TMAS_KEY" --repo olist77/vulnerable-ai-app

# Verify it was added
gh secret list --repo olist77/vulnerable-ai-app
```

---

## Security Best Practices

### ✅ DO:
- Store API keys only in GitHub Secrets (encrypted)
- Use repository secrets (not environment secrets for sensitive keys)
- Rotate API keys every 90-365 days
- Use minimal required permissions
- Review scan results regularly

### ❌ DON'T:
- Commit API keys to repository
- Share API keys in plain text
- Use admin API keys for scanning
- Store keys in workflow files
- Expose keys in logs

---

## Additional Resources

### Trend Vision One Documentation
- **API Keys**: https://docs.trendmicro.com/en-us/enterprise/trend-vision-one/api-keys.aspx
- **TMAS Action**: https://github.com/marketplace/actions/trend-micro-artifact-scanner

### GitHub Documentation
- **Encrypted Secrets**: https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **GitHub Actions**: https://docs.github.com/en/actions

---

## Support

If you encounter issues:

1. Check Vision One API key status in console
2. Review GitHub Actions logs for error messages
3. Verify secret name matches exactly: `TMAS_API_KEY`
4. Contact Trend Micro support with:
   - Workflow run URL
   - Error message from logs
   - Vision One region

---

**Last Updated**: 2026-03-19  
**Repository**: https://github.com/olist77/vulnerable-ai-app  
**Status**: Ready for TMAS scanning
