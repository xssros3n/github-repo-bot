# 📋 Complete Setup Guide

## Step-by-Step Installation

### Step 1: Install Python

**Windows:**
1. Download Python 3.12+ from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify installation:
```bash
python --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3-pip python3-venv -y
```

**macOS:**
```bash
brew install python@3.12
```

### Step 2: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Choose a name for your bot (e.g., "My GitHub Downloader")
4. Choose a username (must end with 'bot', e.g., "my_github_dl_bot")
5. Copy the token that looks like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
6. Save this token securely

### Step 3: Download Bot Code

**Option A: Using Git**
```bash
git clone <repository-url>
cd github-repo-bot
```

**Option B: Manual Download**
1. Download ZIP from GitHub
2. Extract to desired location
3. Open terminal/command prompt in that folder

### Step 4: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

Wait for all packages to install.

### Step 6: Configure Bot

1. Copy the example environment file:

**Windows:**
```bash
copy .env.example .env
```

**Linux/macOS:**
```bash
cp .env.example .env
```

2. Edit `.env` file:

**Windows:**
```bash
notepad .env
```

**Linux/macOS:**
```bash
nano .env
```

3. Replace `your_bot_token_here` with your actual token from BotFather:

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

4. Save and close the file

### Step 7: Run the Bot

```bash
python bot.py
```

You should see:
```
2024-01-01 12:00:00 - github_bot - INFO - Configuration validated
2024-01-01 12:00:00 - github_bot - INFO - Bot initialized successfully
2024-01-01 12:00:00 - github_bot - INFO - Bot started successfully!
```

### Step 8: Test the Bot

1. Open Telegram
2. Search for your bot username
3. Send `/start` command
4. Send a GitHub URL: `https://github.com/octocat/Hello-World`
5. Bot should download and send the ZIP file

## 🎯 Quick Test Commands

```
/start
/help
/stats
https://github.com/octocat/Hello-World
```

## 🔧 Advanced Configuration

### Increase Rate Limits

Edit `.env`:
```env
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60
```

### Increase File Size Limit

Edit `.env`:
```env
MAX_FILE_SIZE_MB=100
```

### Add GitHub Token (Optional)

This increases GitHub API rate limits from 60 to 5000 requests/hour.

1. Go to [GitHub Settings > Developer Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name (e.g., "Telegram Bot")
4. No scopes needed for public repos
5. Generate and copy the token
6. Add to `.env`:

```env
GITHUB_TOKEN=ghp_your_token_here
```

### Enable Debug Logging

Edit `.env`:
```env
LOG_LEVEL=DEBUG
```

## 🖥️ Running 24/7 on VPS

### Using systemd (Linux)

1. Create service file:
```bash
sudo nano /etc/systemd/system/github-bot.service
```

2. Add content (replace paths and username):
```ini
[Unit]
Description=GitHub Repository Downloader Bot
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/home/your-username/github-repo-bot
Environment="PATH=/home/your-username/github-repo-bot/venv/bin"
ExecStart=/home/your-username/github-repo-bot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable github-bot
sudo systemctl start github-bot
```

4. Check status:
```bash
sudo systemctl status github-bot
```

5. View logs:
```bash
sudo journalctl -u github-bot -f
```

### Using screen (Simple Alternative)

1. Install screen:
```bash
sudo apt install screen -y
```

2. Start screen session:
```bash
screen -S github-bot
```

3. Run bot:
```bash
cd github-repo-bot
source venv/bin/activate
python bot.py
```

4. Detach: Press `Ctrl+A` then `D`

5. Reattach later:
```bash
screen -r github-bot
```

## 🐛 Common Issues

### Issue: "No module named 'telegram'"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "TELEGRAM_BOT_TOKEN is required"

**Solution:**
- Check `.env` file exists
- Verify token is correct
- No spaces around `=` in `.env`

### Issue: Bot doesn't respond

**Solution:**
- Check bot is running: `ps aux | grep bot.py`
- Check logs: `tail -f logs/bot_*.log`
- Verify token is correct
- Check internet connection

### Issue: "Repository not found"

**Solution:**
- Ensure repository is public
- Check URL format
- Try in browser first

### Issue: Download timeout

**Solution:**
Edit `.env`:
```env
DOWNLOAD_TIMEOUT=600
```

## 📊 Monitoring

### Check Logs

```bash
# View latest log
tail -f logs/bot_*.log

# Search for errors
grep ERROR logs/bot_*.log

# View specific date
cat logs/bot_20240101.log
```

### Check Disk Space

```bash
df -h
du -sh temp/
```

### Manual Cleanup

```bash
rm temp/*.zip
```

## 🔄 Updating the Bot

1. Stop the bot:
```bash
# If using systemd
sudo systemctl stop github-bot

# If running manually
Ctrl+C
```

2. Pull updates:
```bash
git pull
```

3. Update dependencies:
```bash
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

4. Restart:
```bash
# If using systemd
sudo systemctl start github-bot

# If running manually
python bot.py
```

## 🎓 Next Steps

1. Customize welcome message in `handlers/start_handler.py`
2. Adjust rate limits in `.env`
3. Add your support username in README
4. Set up monitoring/alerts
5. Configure automatic backups

## 💡 Tips

- Keep logs directory clean (old logs can be deleted)
- Monitor disk space in temp directory
- Use GitHub token for better rate limits
- Test with small repositories first
- Keep bot token secret and secure

## 📞 Getting Help

If you encounter issues:
1. Check logs in `logs/` directory
2. Review this guide
3. Check GitHub issues
4. Contact support

---

Happy bot hosting! 🚀
