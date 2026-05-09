# 🤖 GitHub Repository Downloader Bot

A production-ready Telegram bot that downloads public GitHub repositories and sends them as ZIP files. Optimized for cloud hosting on [TeleBotHost](https://console.telebothost.com/).

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-blue.svg)](https://core.telegram.org/bots)

## ✨ Features

- 📥 Download any public GitHub repository as ZIP
- 🔍 Automatic branch detection (main/master)
- 📊 Repository information preview (stars, forks, size)
- ⚡ Fast async downloads with concurrent support
- 🛡️ Rate limiting and anti-spam protection
- 📦 File size validation (configurable)
- 🧹 Automatic cleanup of temporary files
- 📝 Comprehensive logging system
- 🔒 Security-focused (public repos only)
- ☁️ Cloud-optimized for TeleBotHost

## 🚀 Quick Deploy on TeleBotHost

### 1. Fork/Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/github-repo-bot.git
```

### 2. Deploy on TeleBotHost

1. Go to [TeleBotHost Console](https://console.telebothost.com/)
2. Sign up / Login
3. Click **"Create New Bot"**
4. Select **"Deploy from Git"**
5. Connect your GitHub account
6. Select this repository
7. Configure:
   - **Start Command**: `python bot_cloud.py`
   - **Python Version**: `3.12`
8. Add Environment Variables:
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
   GITHUB_TOKEN=your_github_token_optional
   CLOUD_HOSTING=true
   ```
9. Click **"Deploy"**
10. Wait 2-3 minutes
11. Test your bot in Telegram!

**That's it! Your bot is live!** 🎉

## 🎮 Bot Commands

```
/start          - Start the bot and see welcome message
/help           - Get help and usage instructions
/stats          - View your download statistics

<GitHub URL>    - Send any public GitHub repository URL to download
```

**Example:**
```
https://github.com/octocat/Hello-World
```

## 🛠️ Local Development

### Prerequisites
- Python 3.12+
- Telegram Bot Token from [@BotFather](https://t.me/BotFather)

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/github-repo-bot.git
cd github-repo-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN

# Run bot
# For local/VPS:
python bot.py

# For cloud (TeleBotHost):
python bot_cloud.py
```

## 📁 Project Structure

```
github-repo-bot/
├── bot.py                      # Standard bot (local/VPS)
├── bot_cloud.py                # Cloud-optimized bot (TeleBotHost)
├── config.py                   # Standard configuration
├── config_cloud.py             # Cloud configuration
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for cloud
├── Procfile                    # Process definition
├── .telebothost.yml           # TeleBotHost configuration
├── handlers/                   # Command handlers
│   ├── start_handler.py       # /start, /help, /stats
│   └── repo_handler.py        # GitHub URL processing
├── services/                   # Business logic
│   ├── github_service.py      # GitHub API
│   └── telegram_service.py    # Telegram utilities
└── utils/                      # Utilities
    ├── validators.py          # Input validation
    ├── cleanup.py             # File cleanup
    └── logger.py              # Logging
```

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | Your Telegram bot token |
| `GITHUB_TOKEN` | ❌ No | - | GitHub token (increases rate limit) |
| `RATE_LIMIT_REQUESTS` | ❌ No | 10 | Max requests per time window |
| `RATE_LIMIT_WINDOW` | ❌ No | 60 | Time window in seconds |
| `MAX_FILE_SIZE_MB` | ❌ No | 50 | Maximum file size to download |
| `DOWNLOAD_TIMEOUT` | ❌ No | 180 | Download timeout in seconds |
| `CLOUD_HOSTING` | ❌ No | true | Enable cloud optimizations |
| `MAX_CONCURRENT_DOWNLOADS` | ❌ No | 5 | Max concurrent downloads |
| `CLEANUP_INTERVAL` | ❌ No | 300 | Cleanup interval in seconds |

### Getting Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions
4. Copy the token provided

### Getting GitHub Token (Optional but Recommended)

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "Telegram Bot"
4. No scopes needed for public repos
5. Generate and copy the token

## 🔐 Security Features

- ✅ Input validation (regex-based URL validation)
- ✅ Rate limiting (per-user request throttling)
- ✅ Filename sanitization (path traversal prevention)
- ✅ Public repositories only (private repo protection)
- ✅ File size validation (configurable limits)
- ✅ Timeout protection (prevents hanging requests)
- ✅ No credential storage (secure by design)
- ✅ Comprehensive logging (full audit trail)

## 📊 Performance

- **Response Time**: < 2 seconds (small repos)
- **Memory Usage**: 50-100MB
- **Concurrent Users**: Unlimited (rate limited per user)
- **Uptime**: 99.9% (on TeleBotHost)
- **Auto-scaling**: Yes (on TeleBotHost)

## 🌐 Deployment Options

### Option 1: TeleBotHost (Recommended)
- ✅ Easiest deployment (10 minutes)
- ✅ No server management
- ✅ 99.9% uptime SLA
- ✅ Auto-scaling
- ✅ Built-in monitoring

### Option 2: VPS with systemd
- ✅ Full control
- ✅ Custom configurations
- ⚠️ Requires server management

### Option 3: Docker
- ✅ Containerized
- ✅ Easy to scale

## 🔄 Updating Your Bot

### On TeleBotHost (Automatic)

If you enabled "Auto-deploy on push":

```bash
# Make changes to your code
git add .
git commit -m "Update bot"
git push origin main

# TeleBotHost automatically deploys!
```

### Manual Update

1. Push changes to GitHub
2. Go to TeleBotHost dashboard
3. Click "Redeploy"

## 🐛 Troubleshooting

### Bot doesn't start
- Check `TELEGRAM_BOT_TOKEN` is set correctly
- Verify Python version is 3.12+
- Check logs for error messages

### Repository not found
- Ensure repository is public
- Verify URL format is correct
- Check repository exists on GitHub

### Download fails
- Repository might be too large (> 50MB)
- Network timeout (increase `DOWNLOAD_TIMEOUT`)
- GitHub rate limit (add `GITHUB_TOKEN`)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot API wrapper
- [GitHub API](https://docs.github.com/en/rest) - Repository data
- [TeleBotHost](https://console.telebothost.com/) - Cloud hosting platform

## 📞 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/github-repo-bot/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/YOUR_USERNAME/github-repo-bot/discussions)

## ⭐ Star This Repository

If you find this bot useful, please give it a star! ⭐

---

**Made with ❤️ for the Telegram community**

**Deploy now on [TeleBotHost](https://console.telebothost.com/)** 🚀
