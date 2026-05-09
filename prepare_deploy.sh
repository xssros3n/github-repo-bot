#!/bin/bash
# Prepare bot for TeleBotHost deployment

echo "🚀 Preparing GitHub Repo Downloader Bot for TeleBotHost"
echo "=========================================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing git repository..."
    git init
    echo "✅ Git initialized"
else
    echo "✅ Git already initialized"
fi

# Create .gitignore if not exists
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/

# Environment
.env

# Logs
logs/*.log

# Temporary files
temp/*.zip

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
EOF
    echo "✅ .gitignore created"
fi

# Add all files
echo ""
echo "📦 Adding files to git..."
git add .

# Commit
echo "💾 Creating commit..."
git commit -m "Prepare for TeleBotHost deployment" || echo "No changes to commit"

echo ""
echo "=========================================================="
echo "✅ Bot is ready for TeleBotHost deployment!"
echo "=========================================================="
echo ""
echo "Next steps:"
echo "1. Create repository on GitHub/GitLab"
echo "2. Add remote: git remote add origin <your-repo-url>"
echo "3. Push code: git push -u origin main"
echo "4. Go to https://console.telebothost.com/"
echo "5. Create new bot and connect your repository"
echo "6. Add environment variables:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - GITHUB_TOKEN (optional)"
echo "7. Deploy!"
echo ""
echo "📖 Read TELEBOTHOST_DEPLOYMENT.md for detailed instructions"
echo ""
