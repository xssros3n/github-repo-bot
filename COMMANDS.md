# 📋 Project Summary & Commands Reference

## 🎯 Project Overview

**GitHub Repository Downloader Bot** - A production-ready Telegram bot that downloads public GitHub repositories and sends them as ZIP files.

## 📁 Complete File Structure

```
github-repo-bot/
│
├── 📄 Core Files
│   ├── bot.py                    # Main entry point
│   ├── config.py                 # Configuration management
│   └── requirements.txt          # Python dependencies
│
├── 🎮 Handlers (User Interactions)
│   ├── start_handler.py          # /start, /help, /stats commands
│   └── repo_handler.py           # GitHub URL processing & downloads
│
├── 🔧 Services (Business Logic)
│   ├── github_service.py         # GitHub API interactions
│   └── telegram_service.py       # Telegram bot utilities
│
├── 🛠️ Utils (Helper Functions)
│   ├── validators.py             # URL validation & sanitization
│   ├── cleanup.py                # Temp file management
│   └── logger.py                 # Logging configuration
│
├── 📚 Documentation
│   ├── README.md                 # Main documentation
│   ├── QUICKSTART.md             # 5-minute setup guide
│   ├── SETUP_GUIDE.md            # Detailed setup instructions
│   ├── ARCHITECTURE.md           # Code architecture explanation
│   └── TROUBLESHOOTING.md        # Problem solving guide
│
├── 🚀 Deployment
│   ├── .env.example              # Environment variables template
│   ├── Dockerfile                # Docker container config
│   ├── docker-compose.yml        # Docker Compose config
│   ├── github-bot.service        # systemd service template
│   ├── run.bat                   # Windows startup script
│   └── run.sh                    # Linux/macOS startup script
│
├── 📂 Directories
│   ├── logs/                     # Log files (auto-generated)
│   └── temp/                     # Temporary ZIP files
│
└── 🔒 Other
    └── .gitignore                # Git ignore rules
```

## 🚀 Quick Commands Reference

### Initial Setup

```bash
# Clone/Download project
git clone <repo-url>
cd github-repo-bot

# Create virtual environment
python -m venv venv                    # Windows
python3 -m venv venv                   # Linux/macOS

# Activate virtual environment
venv\Scripts\activate                  # Windows
source venv/bin/activate               # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env                   # Linux/macOS
copy .env.example .env                 # Windows
nano .env                              # Edit and add bot token
```

### Running the Bot

```bash
# Simple run
python bot.py

# Using run scripts
run.bat                                # Windows
./run.sh                               # Linux/macOS (chmod +x run.sh first)

# With logging
python bot.py 2>&1 | tee output.log

# In background (Linux/macOS)
nohup python bot.py &

# Stop bot
Ctrl+C                                 # If running in foreground
pkill -f bot.py                        # If running in background
```

### Docker Commands

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down

# Rebuild
docker-compose build --no-cache
docker-compose up -d

# Check status
docker-compose ps
```

### systemd Commands (Linux)

```bash
# Setup service
sudo cp github-bot.service /etc/systemd/system/
sudo nano /etc/systemd/system/github-bot.service  # Edit paths
sudo systemctl daemon-reload

# Control service
sudo systemctl start github-bot
sudo systemctl stop github-bot
sudo systemctl restart github-bot
sudo systemctl status github-bot

# Enable auto-start
sudo systemctl enable github-bot

# View logs
sudo journalctl -u github-bot -f
sudo journalctl -u github-bot -n 100
```

### Maintenance Commands

```bash
# View logs
tail -f logs/bot_*.log
grep ERROR logs/bot_*.log
cat logs/bot_$(date +%Y%m%d).log

# Clean temp files
rm temp/*.zip
python -c "from utils.cleanup import CleanupManager; CleanupManager.cleanup_old_files(0)"

# Check disk space
df -h
du -sh temp/ logs/

# Update dependencies
pip install --upgrade -r requirements.txt
pip list --outdated

# Backup
tar -czf backup-$(date +%Y%m%d).tar.gz .

# Check bot process
ps aux | grep bot.py
top -p $(pgrep -f bot.py)
```

### Testing Commands

```bash
# Test bot token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe

# Test GitHub API
curl https://api.github.com/repos/octocat/Hello-World

# Test Python imports
python -c "import telegram; print(telegram.__version__)"
python -c "from config import config; print('Config OK')"

# Run with debug
LOG_LEVEL=DEBUG python bot.py
```

## 🎮 Bot Commands (In Telegram)

```
/start          - Start bot and see welcome message
/help           - Get help and usage instructions  
/stats          - View your download statistics

<GitHub URL>    - Send any public GitHub repository URL to download
```

## 📝 Configuration Options (.env)

```bash
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional - Rate Limiting
RATE_LIMIT_REQUESTS=5              # Max requests per window
RATE_LIMIT_WINDOW=60               # Time window in seconds

# Optional - File Limits
MAX_FILE_SIZE_MB=50                # Maximum download size

# Optional - Timeouts
DOWNLOAD_TIMEOUT=300               # Download timeout in seconds

# Optional - GitHub API
GITHUB_TOKEN=                      # Increases rate limit to 5000/hour

# Optional - Logging
LOG_LEVEL=INFO                     # DEBUG, INFO, WARNING, ERROR
```

## 🔍 Monitoring Commands

```bash
# Real-time monitoring
watch -n 5 'ps aux | grep bot.py'
watch -n 5 'du -sh temp/'

# Log analysis
grep "Successfully sent" logs/bot_*.log | wc -l    # Count downloads
grep "User" logs/bot_*.log | cut -d' ' -f6 | sort -u | wc -l  # Unique users
grep ERROR logs/bot_*.log | tail -20               # Recent errors

# System resources
htop
free -h
df -h
iostat
```

## 🐛 Debug Commands

```bash
# Check configuration
python -c "from config import config; config.validate(); print('OK')"

# Check imports
python -c "from handlers.start_handler import start_command; print('OK')"
python -c "from services.github_service import GitHubService; print('OK')"

# Test GitHub service
python -c "
import asyncio
from services.github_service import GitHubService
async def test():
    gs = GitHubService()
    info = await gs.get_repo_info('octocat', 'Hello-World')
    print(info['full_name'] if info else 'Failed')
asyncio.run(test())
"

# Check file permissions
ls -la bot.py
ls -la temp/ logs/

# Network tests
ping github.com
ping api.telegram.org
curl -I https://github.com
```

## 📊 Key Features Implemented

✅ **Core Features**
- Download public GitHub repositories
- Automatic branch detection (main/master)
- Repository information preview
- File size validation
- Progress messages

✅ **Security**
- Rate limiting per user
- Input validation & sanitization
- Public repositories only
- Filename sanitization
- Path traversal prevention

✅ **Performance**
- Async/await architecture
- Streaming downloads
- Automatic cleanup
- Connection pooling

✅ **Reliability**
- Comprehensive error handling
- Retry mechanisms
- Timeout handling
- Logging system

✅ **User Experience**
- Clear error messages
- Progress updates
- Statistics tracking
- Help commands

## 🎯 Supported URL Formats

```
✅ https://github.com/owner/repo
✅ https://github.com/owner/repo.git
✅ http://github.com/owner/repo
✅ https://www.github.com/owner/repo

❌ https://gitlab.com/owner/repo
❌ Private repositories
❌ Invalid URLs
```

## 📈 Performance Metrics

- **Concurrent Downloads**: Multiple users simultaneously
- **Download Speed**: Limited by network and GitHub
- **File Size Limit**: Configurable (default 50MB)
- **Rate Limit**: 5 requests per minute per user (configurable)
- **GitHub API**: 60 requests/hour (5000 with token)

## 🔐 Security Features

1. **Input Validation** - Regex-based URL validation
2. **Sanitization** - Filename and path sanitization
3. **Rate Limiting** - Per-user request throttling
4. **Public Only** - Private repository protection
5. **Size Limits** - File size validation
6. **No Credentials** - No sensitive data storage
7. **Auto Cleanup** - Temporary file removal

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Main documentation, features, installation |
| QUICKSTART.md | 5-minute setup guide |
| SETUP_GUIDE.md | Detailed setup and deployment |
| ARCHITECTURE.md | Code structure and explanation |
| TROUBLESHOOTING.md | Problem solving guide |
| This file | Commands reference |

## 🎓 Learning Resources

**Understanding the Code:**
1. Start with `bot.py` - Entry point
2. Read `handlers/start_handler.py` - Simple commands
3. Read `handlers/repo_handler.py` - Main logic
4. Read `services/github_service.py` - API interactions
5. Read `ARCHITECTURE.md` - Full explanation

**Extending the Bot:**
1. Add new command in `handlers/`
2. Register in `bot.py`
3. Test and deploy

## 🚀 Deployment Options

1. **Local Development** - Run directly with `python bot.py`
2. **VPS with systemd** - Production Linux deployment
3. **Docker** - Containerized deployment
4. **PM2** - Node.js process manager
5. **Screen/tmux** - Simple background process

## 📞 Support & Resources

- **Documentation**: Read all .md files
- **Logs**: Check `logs/` directory
- **Issues**: Report on GitHub
- **Updates**: Pull latest changes

## ⚡ Performance Tips

1. Add GitHub token for higher rate limits
2. Adjust file size limits based on needs
3. Monitor disk space regularly
4. Clean temp files periodically
5. Use systemd for auto-restart
6. Enable log rotation
7. Monitor system resources

## 🎯 Next Steps After Setup

1. ✅ Test all commands
2. ✅ Try downloading various repositories
3. ✅ Monitor logs for errors
4. ✅ Set up systemd service (production)
5. ✅ Configure log rotation
6. ✅ Set up monitoring
7. ✅ Customize welcome messages
8. ✅ Add your support contact

## 📝 Version Information

- **Python**: 3.12+
- **python-telegram-bot**: 21.0.1
- **aiohttp**: 3.9.3
- **requests**: 2.31.0

## 🏆 Production Checklist

- [ ] Bot token configured
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Bot tested locally
- [ ] systemd service configured (if Linux)
- [ ] Auto-start enabled
- [ ] Logs monitored
- [ ] Disk space checked
- [ ] Backup configured
- [ ] Documentation read

---

**Ready to start?** → Read [QUICKSTART.md](QUICKSTART.md)

**Need help?** → Read [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

**Want to understand code?** → Read [ARCHITECTURE.md](ARCHITECTURE.md)
