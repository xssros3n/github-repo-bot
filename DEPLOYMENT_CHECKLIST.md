# 🚀 Deployment Checklist

## Pre-Deployment

### Local Testing
- [ ] Bot runs locally without errors
- [ ] All commands work (/start, /help, /stats)
- [ ] Can download small repository
- [ ] Can download medium repository
- [ ] Invalid URLs show proper errors
- [ ] Private repos show proper errors
- [ ] Rate limiting works
- [ ] Logs are being created
- [ ] Temp files are cleaned up

### Configuration
- [ ] `.env` file created from `.env.example`
- [ ] `TELEGRAM_BOT_TOKEN` set correctly
- [ ] Rate limits configured appropriately
- [ ] File size limits set
- [ ] GitHub token added (optional but recommended)
- [ ] Log level set (INFO for production)

### Code Review
- [ ] No hardcoded credentials
- [ ] No debug print statements
- [ ] Error handling in place
- [ ] Logging configured
- [ ] All imports working

## Server Setup

### Server Requirements
- [ ] Ubuntu 20.04+ / Debian 11+ / CentOS 8+
- [ ] Python 3.12+ installed
- [ ] At least 1GB RAM
- [ ] At least 10GB free disk space
- [ ] Stable internet connection
- [ ] SSH access configured

### Server Preparation
```bash
# Update system
- [ ] sudo apt update && sudo apt upgrade -y

# Install dependencies
- [ ] sudo apt install python3.12 python3-pip python3-venv git -y

# Create user (optional but recommended)
- [ ] sudo adduser botuser
- [ ] sudo usermod -aG sudo botuser
- [ ] su - botuser
```

### Upload Code
```bash
# Option 1: Git
- [ ] git clone <your-repo-url>
- [ ] cd github-repo-bot

# Option 2: SCP
- [ ] scp -r github-repo-bot/ user@server:/home/user/

# Option 3: SFTP
- [ ] Use FileZilla or similar
```

### Setup on Server
```bash
- [ ] cd github-repo-bot
- [ ] python3 -m venv venv
- [ ] source venv/bin/activate
- [ ] pip install -r requirements.txt
- [ ] cp .env.example .env
- [ ] nano .env  # Add bot token
- [ ] python verify_setup.py  # Verify installation
```

## Deployment Method

### Choose ONE deployment method:

#### Option A: systemd (Recommended for Production)

```bash
# 1. Edit service file
- [ ] nano github-bot.service
- [ ] Update User=YOUR_USERNAME
- [ ] Update WorkingDirectory=/full/path/to/github-repo-bot
- [ ] Update Environment path
- [ ] Update ExecStart path

# 2. Install service
- [ ] sudo cp github-bot.service /etc/systemd/system/
- [ ] sudo systemctl daemon-reload
- [ ] sudo systemctl enable github-bot
- [ ] sudo systemctl start github-bot

# 3. Verify
- [ ] sudo systemctl status github-bot
- [ ] sudo journalctl -u github-bot -f
```

#### Option B: Docker

```bash
# 1. Install Docker
- [ ] curl -fsSL https://get.docker.com -o get-docker.sh
- [ ] sudo sh get-docker.sh
- [ ] sudo usermod -aG docker $USER

# 2. Install Docker Compose
- [ ] sudo apt install docker-compose -y

# 3. Deploy
- [ ] docker-compose build
- [ ] docker-compose up -d

# 4. Verify
- [ ] docker-compose ps
- [ ] docker-compose logs -f
```

#### Option C: Screen (Simple but not recommended for production)

```bash
- [ ] sudo apt install screen -y
- [ ] screen -S github-bot
- [ ] cd github-repo-bot
- [ ] source venv/bin/activate
- [ ] python bot.py
- [ ] Press Ctrl+A then D to detach
```

## Post-Deployment

### Verification
- [ ] Bot is running (check with ps aux | grep bot.py)
- [ ] Bot responds in Telegram
- [ ] Can download a test repository
- [ ] Logs are being written
- [ ] No errors in logs

### Monitoring Setup

#### Log Rotation
```bash
- [ ] sudo nano /etc/logrotate.d/github-bot
```

Add:
```
/home/user/github-repo-bot/logs/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
```

#### Disk Space Monitoring
```bash
- [ ] Add to crontab: crontab -e
```

Add:
```bash
# Clean temp files daily at 3 AM
0 3 * * * cd /path/to/github-repo-bot && /path/to/venv/bin/python -c "from utils.cleanup import CleanupManager; CleanupManager.cleanup_old_files(1)"

# Check disk space daily
0 6 * * * df -h | grep -E '^/dev/' | awk '{if($5+0 > 80) print "Disk usage high: "$0}' | mail -s "Disk Alert" your@email.com
```

#### Health Check Script
```bash
- [ ] Create health_check.sh
```

```bash
#!/bin/bash
if ! pgrep -f "bot.py" > /dev/null; then
    echo "Bot is down! Restarting..."
    systemctl restart github-bot
    echo "Bot restarted at $(date)" >> /var/log/bot-restarts.log
fi
```

```bash
- [ ] chmod +x health_check.sh
- [ ] Add to crontab: */5 * * * * /path/to/health_check.sh
```

### Security Hardening

#### Firewall
```bash
- [ ] sudo ufw allow ssh
- [ ] sudo ufw allow 443/tcp
- [ ] sudo ufw enable
- [ ] sudo ufw status
```

#### File Permissions
```bash
- [ ] chmod 600 .env
- [ ] chmod 755 bot.py
- [ ] chmod 755 logs/
- [ ] chmod 755 temp/
```

#### Fail2ban (Optional)
```bash
- [ ] sudo apt install fail2ban -y
- [ ] sudo systemctl enable fail2ban
- [ ] sudo systemctl start fail2ban
```

### Backup Setup

#### Automated Backup Script
```bash
- [ ] Create backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/user/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/github-bot-$DATE.tar.gz \
    --exclude='venv' \
    --exclude='temp/*.zip' \
    --exclude='logs/*.log' \
    /path/to/github-repo-bot
# Keep only last 7 backups
ls -t $BACKUP_DIR/github-bot-*.tar.gz | tail -n +8 | xargs rm -f
```

```bash
- [ ] chmod +x backup.sh
- [ ] Add to crontab: 0 2 * * * /path/to/backup.sh
```

## Monitoring & Maintenance

### Daily Checks
- [ ] Check bot is running
- [ ] Check logs for errors
- [ ] Check disk space
- [ ] Check system resources

### Weekly Checks
- [ ] Review error logs
- [ ] Check backup integrity
- [ ] Update dependencies if needed
- [ ] Clean old logs manually

### Monthly Checks
- [ ] Review and optimize configuration
- [ ] Check for bot updates
- [ ] Review security patches
- [ ] Analyze usage statistics

## Troubleshooting Commands

```bash
# Check if bot is running
- [ ] ps aux | grep bot.py
- [ ] sudo systemctl status github-bot

# View logs
- [ ] tail -f logs/bot_*.log
- [ ] sudo journalctl -u github-bot -f

# Restart bot
- [ ] sudo systemctl restart github-bot

# Check disk space
- [ ] df -h
- [ ] du -sh temp/ logs/

# Check system resources
- [ ] htop
- [ ] free -h

# Test bot manually
- [ ] source venv/bin/activate
- [ ] python bot.py
```

## Rollback Plan

### If deployment fails:

```bash
# 1. Stop the bot
- [ ] sudo systemctl stop github-bot

# 2. Restore from backup
- [ ] cd /home/user
- [ ] tar -xzf backups/github-bot-YYYYMMDD_HHMMSS.tar.gz

# 3. Restart
- [ ] sudo systemctl start github-bot

# 4. Verify
- [ ] sudo systemctl status github-bot
```

## Performance Optimization

### For High Traffic
```bash
# Increase rate limits in .env
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# Add GitHub token
GITHUB_TOKEN=your_token_here

# Increase system limits
- [ ] sudo nano /etc/security/limits.conf
```

Add:
```
* soft nofile 65536
* hard nofile 65536
```

### For Large Files
```bash
# Increase timeouts in .env
DOWNLOAD_TIMEOUT=600
MAX_FILE_SIZE_MB=100
```

## Documentation

### Update Documentation
- [ ] Update README.md with your bot username
- [ ] Add your support contact
- [ ] Document any custom changes
- [ ] Update deployment notes

### Share with Team
- [ ] Share server access details (securely)
- [ ] Share bot token (securely)
- [ ] Share monitoring dashboard access
- [ ] Document any custom procedures

## Final Verification

### Functionality Test
- [ ] Send /start to bot
- [ ] Send /help to bot
- [ ] Send /stats to bot
- [ ] Download small repo (< 1MB)
- [ ] Download medium repo (5-10MB)
- [ ] Test with invalid URL
- [ ] Test rate limiting (send 6 requests quickly)

### Performance Test
- [ ] Check response time
- [ ] Check download speed
- [ ] Check memory usage
- [ ] Check CPU usage

### Monitoring Test
- [ ] Logs are being written
- [ ] Log rotation works
- [ ] Backup script works
- [ ] Health check works
- [ ] Alerts work (if configured)

## Go Live Checklist

- [ ] All tests passed
- [ ] Monitoring configured
- [ ] Backups configured
- [ ] Documentation updated
- [ ] Team notified
- [ ] Support contact added to bot
- [ ] Bot username shared with users
- [ ] Emergency contacts ready

## Post-Launch

### First 24 Hours
- [ ] Monitor logs continuously
- [ ] Check for errors
- [ ] Verify all features work
- [ ] Monitor system resources
- [ ] Be ready for quick fixes

### First Week
- [ ] Daily log reviews
- [ ] Monitor user feedback
- [ ] Track usage statistics
- [ ] Optimize if needed
- [ ] Document any issues

### First Month
- [ ] Weekly performance reviews
- [ ] Analyze usage patterns
- [ ] Plan improvements
- [ ] Update documentation
- [ ] Celebrate success! 🎉

---

## Emergency Contacts

- Server Provider: _______________
- Domain Provider: _______________
- Team Lead: _______________
- On-Call Person: _______________

## Important URLs

- Server IP: _______________
- Monitoring Dashboard: _______________
- Backup Location: _______________
- Documentation: _______________

---

**Remember:** Always test in a staging environment before deploying to production!

**Good luck with your deployment! 🚀**
