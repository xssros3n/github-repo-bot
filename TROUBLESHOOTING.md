# 🔧 Troubleshooting Guide

## Installation Issues

### Python Version Error

**Error:** `Python 3.12 or higher is required`

**Solution:**
```bash
# Check version
python --version

# Install Python 3.12+
# Windows: Download from python.org
# Linux: sudo apt install python3.12
# macOS: brew install python@3.12
```

### pip Not Found

**Error:** `pip: command not found`

**Solution:**
```bash
# Windows
python -m pip install --upgrade pip

# Linux/macOS
python3 -m pip install --upgrade pip
```

### Virtual Environment Issues

**Error:** `venv: command not found`

**Solution:**
```bash
# Linux/macOS
sudo apt install python3-venv

# Then create venv
python3 -m venv venv
```

### Permission Denied

**Error:** `Permission denied` when creating directories

**Solution:**
```bash
# Linux/macOS
sudo chown -R $USER:$USER .
chmod -R 755 .

# Or run with sudo (not recommended)
sudo python bot.py
```

## Configuration Issues

### Missing .env File

**Error:** `TELEGRAM_BOT_TOKEN is required in .env file`

**Solution:**
```bash
# Copy example file
cp .env.example .env

# Edit and add your token
nano .env
```

### Invalid Bot Token

**Error:** Bot doesn't start or `Unauthorized`

**Solution:**
1. Check token has no spaces
2. Verify token from @BotFather
3. Generate new token if needed:
   - Send `/token` to @BotFather
   - Select your bot
   - Copy new token

### Environment Variables Not Loading

**Error:** Bot uses default values instead of .env

**Solution:**
```bash
# Ensure .env is in same directory as bot.py
ls -la .env

# Check file format (no BOM, UTF-8)
file .env

# Verify no spaces around =
# Wrong: TOKEN = 123
# Right: TOKEN=123
```

## Runtime Issues

### Bot Doesn't Respond

**Symptoms:** Bot online but doesn't reply

**Diagnosis:**
```bash
# Check if bot is running
ps aux | grep bot.py

# Check logs
tail -f logs/bot_*.log

# Test bot token
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

**Solutions:**
1. Restart bot
2. Check internet connection
3. Verify token is correct
4. Check Telegram API status

### Rate Limit Errors

**Error:** `429 Too Many Requests`

**Solution:**
```bash
# Edit .env
RATE_LIMIT_REQUESTS=3
RATE_LIMIT_WINDOW=120

# Or add GitHub token
GITHUB_TOKEN=your_github_token
```

### Download Timeout

**Error:** `Download timeout for owner/repo`

**Solution:**
```bash
# Increase timeout in .env
DOWNLOAD_TIMEOUT=600

# Or try smaller repository
```

### File Too Large

**Error:** `Repository too large!`

**Solution:**
```bash
# Increase limit in .env (be careful with Telegram limits)
MAX_FILE_SIZE_MB=100

# Note: Telegram has 50MB limit for bots
# Consider using file splitting for larger repos
```

### Repository Not Found

**Error:** `Repository not found!`

**Checklist:**
- [ ] Repository exists on GitHub
- [ ] Repository is public (not private)
- [ ] URL is correct format
- [ ] No typos in owner/repo name

**Test:**
```bash
# Try in browser first
https://github.com/owner/repo

# Check with curl
curl https://api.github.com/repos/owner/repo
```

### Private Repository Error

**Error:** `Private Repository - Sorry, I can only download public repositories`

**Solution:**
- This is intentional - bot only supports public repos
- Make repository public on GitHub
- Or fork it as public repository

## Network Issues

### Connection Timeout

**Error:** `Timeout getting repo info`

**Solutions:**
```bash
# Check internet connection
ping github.com
ping api.telegram.org

# Check firewall
# Windows: Allow Python in Windows Firewall
# Linux: sudo ufw allow out 443/tcp

# Check proxy settings if behind corporate firewall
```

### SSL Certificate Error

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Solution:**
```bash
# Update certificates
pip install --upgrade certifi

# Or disable SSL verification (not recommended)
# Add to github_service.py:
# ssl=False in aiohttp.ClientSession
```

## Disk Space Issues

### No Space Left

**Error:** `No space left on device`

**Solution:**
```bash
# Check disk space
df -h

# Clean temp directory
rm temp/*.zip

# Clean old logs
rm logs/bot_*.log

# Or run cleanup
python -c "from utils.cleanup import CleanupManager; CleanupManager.cleanup_old_files(0)"
```

### Permission to Write

**Error:** `Permission denied` when writing files

**Solution:**
```bash
# Check directory permissions
ls -la temp/ logs/

# Fix permissions
chmod 755 temp/ logs/
```

## Deployment Issues

### systemd Service Won't Start

**Error:** `Failed to start github-bot.service`

**Diagnosis:**
```bash
# Check status
sudo systemctl status github-bot

# Check logs
sudo journalctl -u github-bot -n 50

# Test manually
cd /path/to/bot
source venv/bin/activate
python bot.py
```

**Common Issues:**
1. Wrong paths in service file
2. Wrong user
3. Missing .env file
4. Virtual environment not activated

**Solution:**
```bash
# Edit service file
sudo nano /etc/systemd/system/github-bot.service

# Verify paths are absolute
# Verify user exists
# Reload and restart
sudo systemctl daemon-reload
sudo systemctl restart github-bot
```

### Docker Issues

**Error:** Container exits immediately

**Solution:**
```bash
# Check logs
docker logs github-repo-bot

# Check .env file exists
ls -la .env

# Rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# View logs
docker-compose logs -f
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port
lsof -i :8443

# Kill process
kill -9 <PID>

# Or use different port
```

## Performance Issues

### Bot is Slow

**Symptoms:** Long response times

**Solutions:**
1. Check server resources:
```bash
top
htop
free -h
```

2. Optimize configuration:
```bash
# Reduce timeout
DOWNLOAD_TIMEOUT=120

# Reduce file size limit
MAX_FILE_SIZE_MB=25
```

3. Check network speed:
```bash
speedtest-cli
```

### High Memory Usage

**Solution:**
```bash
# Monitor memory
watch -n 1 free -h

# Restart bot periodically
# Add to crontab:
0 3 * * * systemctl restart github-bot
```

### High CPU Usage

**Solution:**
```bash
# Check what's using CPU
top -p $(pgrep -f bot.py)

# Reduce concurrent operations
# Add rate limiting
```

## Logging Issues

### No Logs Created

**Solution:**
```bash
# Check logs directory exists
ls -la logs/

# Check permissions
chmod 755 logs/

# Check config
python -c "from config import config; print(config.LOGS_DIR)"
```

### Logs Too Large

**Solution:**
```bash
# Rotate logs manually
cd logs/
gzip bot_*.log

# Or setup logrotate
sudo nano /etc/logrotate.d/github-bot
```

Add:
```
/path/to/github-repo-bot/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

## GitHub API Issues

### Rate Limit Exceeded

**Error:** `API rate limit exceeded`

**Solution:**
```bash
# Add GitHub token to .env
GITHUB_TOKEN=ghp_your_token_here

# Check current rate limit
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/rate_limit
```

### API Not Responding

**Error:** `GitHub API error: 500`

**Solution:**
- Wait and retry (GitHub might be down)
- Check GitHub status: https://www.githubstatus.com/
- Implement retry logic (already included)

## Telegram API Issues

### Flood Control

**Error:** `Too many requests: retry after X`

**Solution:**
- Bot automatically handles this
- Reduce request frequency
- Wait before retrying

### File Too Large for Telegram

**Error:** `File too large` when sending

**Solution:**
- Telegram bot limit is 50MB
- Reduce MAX_FILE_SIZE_MB in .env
- Consider file splitting (advanced)

## Code Issues

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'X'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or install specific module
pip install module-name
```

### Syntax Errors

**Error:** `SyntaxError: invalid syntax`

**Solution:**
- Check Python version (must be 3.12+)
- Check file encoding (must be UTF-8)
- Verify no copy-paste errors

### Async Errors

**Error:** `RuntimeError: Event loop is closed`

**Solution:**
```bash
# Update aiohttp
pip install --upgrade aiohttp

# Or restart bot
```

## Database Issues (If Added)

### Connection Failed

**Solution:**
```bash
# Check database is running
sudo systemctl status postgresql

# Check connection string
# Verify credentials
```

## Getting Help

### Before Asking for Help

1. Check logs:
```bash
tail -f logs/bot_*.log
```

2. Test manually:
```bash
python bot.py
# Try commands in Telegram
```

3. Verify configuration:
```bash
cat .env
```

4. Check system resources:
```bash
df -h
free -h
top
```

### Information to Provide

When asking for help, include:
- Error message (full text)
- Relevant logs
- Python version
- Operating system
- Steps to reproduce
- What you've tried

### Useful Commands

```bash
# System info
uname -a
python --version
pip list

# Bot status
ps aux | grep bot.py
systemctl status github-bot

# Logs
tail -n 100 logs/bot_*.log
grep ERROR logs/bot_*.log

# Network
ping github.com
curl https://api.telegram.org/botTOKEN/getMe

# Disk
df -h
du -sh temp/ logs/
```

## Emergency Recovery

### Bot Completely Broken

```bash
# 1. Stop bot
pkill -f bot.py
# or
sudo systemctl stop github-bot

# 2. Backup
cp -r github-repo-bot github-repo-bot.backup

# 3. Clean reinstall
cd github-repo-bot
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Verify config
cat .env

# 5. Test
python bot.py

# 6. If works, restart service
sudo systemctl start github-bot
```

### Reset Everything

```bash
# Nuclear option - start fresh
cd ..
rm -rf github-repo-bot/
git clone <repo-url>
cd github-repo-bot
# Follow QUICKSTART.md
```

## Prevention

### Best Practices

1. **Regular Backups**
```bash
# Backup script
tar -czf backup-$(date +%Y%m%d).tar.gz github-repo-bot/
```

2. **Monitor Logs**
```bash
# Daily log check
grep ERROR logs/bot_*.log | tail -20
```

3. **Update Dependencies**
```bash
# Monthly update
pip list --outdated
pip install --upgrade -r requirements.txt
```

4. **Clean Temp Files**
```bash
# Weekly cleanup
find temp/ -name "*.zip" -mtime +7 -delete
```

5. **Monitor Resources**
```bash
# Setup monitoring
# Use tools like: htop, netdata, prometheus
```

---

Still having issues? Check:
- [README.md](README.md) - Full documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Setup instructions
- [ARCHITECTURE.md](ARCHITECTURE.md) - Code explanation
- GitHub Issues - Report bugs
