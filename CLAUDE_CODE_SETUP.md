# Claude Code GitHub Integration Setup Guide

## 🎯 Overview

This guide will help you set up Claude Code integration with your GitHub repository to get AI-powered code reviews on pull requests.

---

## ✅ What You've Already Done

You've successfully generated your Claude OAuth token:
```
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
```
⏰ **Valid for 1 year**

---

## 📋 Setup Steps

### Step 1: Add the GitHub Secret

1. **Go to your repository settings:**
   ```
   https://github.com/olist77/vulnerable-ai-app/settings/secrets/actions
   ```

2. **Click "New repository secret"**

3. **Add the secret:**
   - **Name:** `CLAUDE_API_KEY`
   - **Value:** `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`

4. **Click "Add secret"**

### Step 2: Push the Workflow File

The workflow file has been created at:
```
.github/workflows/claude-code.yml
```

Push it to GitHub:
```bash
cd /Users/stefanoolivieri/Downloads/vulnerable-ai-app

git add .github/workflows/claude-code.yml
git add CLAUDE_CODE_SETUP.md
git commit -m "Add Claude Code review workflow"
git push origin main
```

### Step 3: Test the Integration

Create a test pull request to verify it works:

```bash
# Create a new branch
git checkout -b test-claude-review

# Make a small change
echo "# Test change for Claude Code review" >> test-file.md

# Commit and push
git add test-file.md
git commit -m "Test: Claude Code review integration"
git push origin test-claude-review
```

Then create a PR on GitHub:
```
https://github.com/olist77/vulnerable-ai-app/compare/main...test-claude-review
```

---

## 🎬 How It Works

### When the Workflow Triggers:

The workflow will run automatically on:
- ✅ New pull requests
- ✅ Updates to existing PRs (new commits)
- ✅ Reopened PRs
- ✅ Manual trigger via GitHub Actions UI

### What Claude Code Will Do:

1. **Checkout your code** with full git history
2. **Analyze the changes** in the PR
3. **Post review comments** directly on the PR with:
   - Security vulnerabilities
   - Code quality issues
   - Best practice suggestions
   - Potential bugs
   - Performance improvements

### Example Review Comment:

```
🤖 Claude Code Review

**Security Issue Found:**
Line 15: Hardcoded API key detected
`OPENAI_API_KEY = "sk-proj-..."`

**Recommendation:**
Use environment variables or a secrets manager instead:
`OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')`

**Severity:** HIGH
```

---

## 🔧 Workflow Configuration

### Current Settings:

```yaml
name: Claude Code Review

on:
  pull_request:
    types: [opened, synchronize, reopened]
  workflow_dispatch:  # Manual trigger

permissions:
  contents: read
  pull-requests: write  # Post comments
  issues: write

jobs:
  claude-review:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history for context

      - name: Claude Code Action
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.CLAUDE_API_KEY }}
```

### Optional Customizations:

You can customize the review by uncommenting and modifying these options:

```yaml
# Custom review prompt
prompt: |
  Review this code focusing on:
  - Security vulnerabilities (SQL injection, XSS, etc.)
  - AI/ML specific issues (prompt injection, model poisoning)
  - Best practices for Python/Flask applications
  - Performance bottlenecks

# Include specific file patterns
include_patterns: "*.py,*.js,*.yml,Dockerfile"

# Exclude files from review
exclude_patterns: "tests/**,*.min.js,node_modules/**"
```

---

## 📊 Expected Results for vulnerable-ai-app

Given that your app is **intentionally vulnerable**, Claude Code should detect:

### Security Issues (50+):
- ❌ Hardcoded API keys and secrets
- ❌ SQL injection vulnerabilities
- ❌ Command injection (os.system, subprocess)
- ❌ Insecure deserialization (pickle.load)
- ❌ Use of eval() on user input
- ❌ Template injection (render_template_string)
- ❌ Path traversal vulnerabilities
- ❌ Debug mode in production
- ❌ Exposed configuration endpoints

### AI-Specific Issues:
- ❌ Prompt injection vulnerabilities
- ❌ No input sanitization for LLM prompts
- ❌ Unsafe model loading
- ❌ No rate limiting on AI endpoints
- ❌ eval() on AI-generated code

### Best Practice Violations:
- ❌ No input validation
- ❌ No authentication/authorization
- ❌ Overly permissive CORS
- ❌ Detailed error messages with stack traces
- ❌ Running as root in containers

---

## 🔍 Monitoring the Workflow

### Check Workflow Status:

1. **Actions Tab:**
   ```
   https://github.com/olist77/vulnerable-ai-app/actions
   ```

2. **PR Checks:**
   - Look for "Claude Code Review" check on your PR
   - ✅ Green check = review completed
   - ❌ Red X = workflow failed

3. **Review Comments:**
   - Claude will post inline comments on changed lines
   - Summary comment at the bottom of the PR

### Debugging Issues:

If the workflow fails:

1. **Check the workflow logs:**
   - Go to Actions tab
   - Click on the failed run
   - Review logs for errors

2. **Common Issues:**
   - Invalid API key (check secret name: `CLAUDE_API_KEY`)
   - Permissions issue (ensure PR write access)
   - API rate limiting (wait and retry)

---

## 🎓 Best Practices

### For Real Projects (Not This Demo):

1. **Enable branch protection:**
   - Require Claude Code review before merging
   - Settings → Branches → Add rule

2. **Customize the prompt:**
   - Focus on your stack (Python/Flask/ML)
   - Add company-specific guidelines
   - Include security requirements

3. **Filter files:**
   - Exclude test files if desired
   - Focus on critical paths
   - Ignore generated code

4. **Review regularly:**
   - Don't blindly accept all suggestions
   - Use Claude as a "second pair of eyes"
   - Learn from the feedback

---

## 🔐 Security Notes

### About Your OAuth Token:

- ✅ **Stored securely** in GitHub Secrets (encrypted)
- ✅ **Valid for 1 year** (expires 2027-03-19)
- ✅ **Scoped access** (only what Claude Code needs)
- 🔄 **Renewable** via `claude setup-token` when expired

### Token Permissions:

Your token can:
- ✅ Read repository contents
- ✅ Post PR comments
- ✅ Read/write to Issues

Your token **cannot**:
- ❌ Push code
- ❌ Modify repository settings
- ❌ Access other organizations
- ❌ Delete anything

### Token Revocation:

If you need to revoke the token:
```bash
# Generate new token
claude setup-token

# Update GitHub secret with new token
# Delete old token from Anthropic console
```

---

## 📚 Additional Resources

### Documentation:
- **Claude Code Action:** https://github.com/anthropics/claude-code-action
- **GitHub Actions Secrets:** https://docs.github.com/en/actions/security-guides/encrypted-secrets
- **Claude API:** https://docs.anthropic.com/claude/reference

### Example Workflows:
- **Basic Review:** https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml
- **Advanced Config:** https://github.com/anthropics/claude-code-action/blob/main/examples/advanced.yml

---

## 🎯 Next Steps

1. ✅ **Add the GitHub secret** (`CLAUDE_API_KEY`)
2. ✅ **Push the workflow file** to GitHub
3. ✅ **Create a test PR** to verify
4. 📊 **Review Claude's feedback** on your vulnerable code
5. 🎓 **Learn from the patterns** it identifies

---

## ❓ Troubleshooting

### Issue: "Secret CLAUDE_API_KEY not found"
**Solution:** Verify the secret name is exactly `CLAUDE_API_KEY` (case-sensitive)

### Issue: "Invalid API key"
**Solution:** 
- Check you copied the full token (starts with `sk-ant-oat01-`)
- Regenerate token if needed: `claude setup-token`

### Issue: "Permission denied"
**Solution:** 
- Check workflow has `pull-requests: write` permission
- Verify GitHub token has necessary scopes

### Issue: "Workflow not triggering"
**Solution:**
- Push workflow file to default branch (main)
- Check workflow is enabled in Actions tab
- Verify PR is from correct branch

---

## 🎉 Success Checklist

- [ ] GitHub secret `CLAUDE_API_KEY` added
- [ ] Workflow file `.github/workflows/claude-code.yml` pushed
- [ ] Test PR created
- [ ] Claude Code review appeared on PR
- [ ] Review comments are visible
- [ ] Workflow shows green checkmark

---

**Last Updated:** 2026-03-19  
**Claude Code Version:** Compatible with v2.1.22+  
**Token Expiry:** 2027-03-19 (1 year from generation)
