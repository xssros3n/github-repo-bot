# ⚡ TeleBotHost Quick Start Guide

## 🎯 Deploy Your Bot in 10 Minutes!

### Prerequisites
- ✅ GitHub account
- ✅ Telegram bot token from @BotFather
- ✅ 10 minutes of your time

---

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Code (2 minutes)

**Windows:**
```bash
prepare_deploy.bat
```

**Linux/macOS:**
```bash
chmod +x prepare_deploy.sh
./prepare_deploy.sh
```

This will:
- Initialize git repository
- Add all files
- Create initial commit

### Step 2: Push to GitHub (3 minutes)

```bash
# Create repository on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/github-repo-bot.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy on TeleBotHost (5 minutes)

1. **Sign Up**
   - Go to https://console.telebothost.com/
   - Click "Sign Up"
   - Verify email

2. **Create Bot**
   - Click "Create New Bot"
   - Name: "GitHub Repo Downloader"
   - Select "Deploy from Git"

3. **Connect Repository**
   - Connect GitHub account
   - Select your repository
   - Select branch: `main`

4. **Configure**
   - Start Command: `python bot_cloud.py`
   - Python Version: `3.12`

5. **Add Environment Variables**
   ```
   TELEGRAM_BOT_TOKEN = your_bot_token_here
   GITHUB_TOKEN = your_github_token (optional)
   CLOUD_HOSTING = true
   ```

6. **Deploy**
   - Click "Deploy Bot"
   - Wait 2-3 minutes
   - Check logs for "Bot started successfully!"

7. **Test**
   - Open Telegram
   - Find your bot
   - Send `/start`
   - Try downloading a repo!

---

## ✅ Verification Checklist

- [ ] Bot shows as "Running" in dashboard
- [ ] Logs show "Bot started successfully on TeleBotHost!"
- [ ] Bot responds to `/start` in Telegram
- [ ] Can download a test repository
- [ ] No errors in logs

---

## 🎛️ Dashboard Overview

### Main Dashboard
- **Status**: Bot running status
- **Uptime**: Current uptime percentage
- **Requests**: Total requests handled
- **Errors**: Error count

### Logs Tab
- Real-time log streaming
- Filter by level (INFO, ERROR, etc.)
- Download logs
- Search functionality

### Settings Tab
- Environment variables
- Resource allocation
- Auto-restart settings
- Scaling configuration

### Metrics Tab
- CPU usage
- Memory usage
- Network traffic
- Response times

---

## 🔧 Common Configurations

### Increase Rate Limits
```
Dashboard > Settings > Environment Variables
RATE_LIMIT_REQUESTS = 20
```

### Increase File Size Limit
```
Dashboard > Settings > Environment Variables
MAX_FILE_SIZE_MB = 100
```

### Enable More Concurrent Downloads
```
Dashboard > Settings > Environment Variables
MAX_CONCURRENT_DOWNLOADS = 10
```

### Adjust Cleanup Frequency
```
Dashboard > Settings > Environment Variables
CLEANUP_INTERVAL = 600  (10 minutes)
```

---

## 📊 Monitoring

### Set Up Alerts

1. Go to **Dashboard > Alerts**
2. Click "Create Alert"
3. Configure:
   - **High Error Rate**: > 5%
   - **Bot Offline**: Immediate
   - **High Memory**: > 80%
   - **Slow Response**: > 5 seconds

4. Choose notification method:
   - Email
   - Telegram
   - Webhook

### View Metrics

1. Go to **Dashboard > Metrics**
2. View:
   - Request rate
   - Error rate
   - Response time
   - Resource usage

---

## 🔄 Updating Your Bot

### Method 1: Git Push (Recommended)
```bash
# Make changes to your code
git add .
git commit -m "Update bot"
git push origin main

# TeleBotHost auto-deploys!
# Zero downtime deployment
```

### Method 2: Dashboard Upload
1. Go to **Dashboard > Deployment**
2. Click "Upload New Version"
3. Upload ZIP file
4. Click "Deploy"

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check:**
1. Logs for error messages
2. Environment variables are set
3. TELEGRAM_BOT_TOKEN is correct
4. Python version is 3.12

**Fix:**
```
Dashboard > Settings > Environment Variables
Verify all variables are set correctly
Click "Restart Bot"
```

### High Memory Usage

**Solution:**
```
Dashboard > Settings > Resources
Increase memory allocation to 1GB
Or reduce MAX_CONCURRENT_DOWNLOADS to 3
```

### Bot Slow to Respond

**Solution:**
```
Dashboard > Settings > Scaling
Enable auto-scaling
Set min instances: 1
Set max instances: 3
```

### Logs Not Showing

**Solution:**
```
Dashboard > Settings > Logging
Set LOG_LEVEL = DEBUG
Restart bot
```

---

## 💰 Pricing Plans

### Free Tier (Testing)
- 100 MB RAM
- 0.1 CPU
- 1 GB bandwidth
- Good for: Testing only

### Basic Plan ($5-10/month)
- 512 MB RAM
- 1 CPU
- 10 GB bandwidth
- Good for: Small bots (< 100 users)

### Pro Plan ($20-30/month)
- 1 GB RAM
- 2 CPU
- 50 GB bandwidth
- Auto-scaling
- Good for: Production bots (100-1000 users)

### Enterprise (Custom)
- Custom resources
- Dedicated support
- SLA guarantee
- Good for: Large bots (1000+ users)

**Recommendation for this bot:** Start with Basic, upgrade if needed.

---

## 📈 Scaling Strategy

### When to Scale Up?

**Indicators:**
- Memory usage > 80%
- CPU usage > 70%
- Response time > 3 seconds
- Error rate > 2%

### How to Scale?

**Vertical Scaling:**
```
Dashboard > Settings > Resources
Increase RAM/CPU
Apply changes (no downtime)
```

**Horizontal Scaling:**
```
Dashboard > Settings > Scaling
Enable auto-scaling
Min instances: 1
Max instances: 3
Scale trigger: CPU > 70%
```

---

## 🔐 Security Best Practices

### 1. Secure Environment Variables
- Never commit .env to git
- Use TeleBotHost's environment variables
- Rotate tokens regularly

### 2. Enable 2FA
```
Dashboard > Account > Security
Enable Two-Factor Authentication
```

### 3. Monitor Access Logs
```
Dashboard > Security > Access Logs
Review login attempts
Set up alerts for suspicious activity
```

### 4. Use GitHub Token
```
Add GITHUB_TOKEN to environment variables
Increases rate limit from 60 to 5000/hour
```

---

## 📞 Getting Help

### TeleBotHost Support
- **Documentation**: https://docs.telebothost.com/
- **Email**: support@telebothost.com
- **Live Chat**: Available in dashboard
- **Community**: Discord/Telegram group

### Bot-Specific Help
- **Documentation**: Read all .md files in project
- **Troubleshooting**: TROUBLESHOOTING.md
- **GitHub Issues**: Report bugs

---

## ✅ Post-Deployment Checklist

### Immediate (First Hour)
- [ ] Bot is running
- [ ] Responds to commands
- [ ] Can download repositories
- [ ] Logs are clean
- [ ] No errors

### First Day
- [ ] Monitor performance
- [ ] Check error rate
- [ ] Test with multiple users
- [ ] Verify cleanup works
- [ ] Set up alerts

### First Week
- [ ] Review metrics
- [ ] Optimize settings
- [ ] Check costs
- [ ] Gather user feedback
- [ ] Plan improvements

---

## 🎉 Success!

Your bot is now running on TeleBotHost with:
- ✅ 99.9% uptime
- ✅ Automatic scaling
- ✅ Built-in monitoring
- ✅ Zero-downtime updates
- ✅ Professional support

---

## 🚀 Next Steps

1. **Customize Bot**
   - Update welcome message
   - Add your support contact
   - Customize commands

2. **Monitor Performance**
   - Check dashboard daily
   - Review metrics weekly
   - Optimize based on data

3. **Promote Bot**
   - Share with users
   - Gather feedback
   - Iterate and improve

4. **Scale as Needed**
   - Monitor growth
   - Upgrade plan when needed
   - Enable auto-scaling

---

## 💡 Pro Tips

1. ✅ Always use `bot_cloud.py` for TeleBotHost
2. ✅ Set `CLOUD_HOSTING=true` in environment
3. ✅ Add GitHub token for better rate limits
4. ✅ Enable auto-scaling for traffic spikes
5. ✅ Set up alerts for critical issues
6. ✅ Review logs weekly
7. ✅ Keep dependencies updated
8. ✅ Monitor costs monthly

---

## 📖 Additional Resources

- **Full Deployment Guide**: TELEBOTHOST_DEPLOYMENT.md
- **Local vs Cloud**: LOCAL_VS_CLOUD.md
- **Architecture**: ARCHITECTURE.md
- **Troubleshooting**: TROUBLESHOOTING.md

---

**Your bot is production-ready on TeleBotHost!** 🎉

**Questions?** Check the documentation or contact support!

**Happy hosting!** 🚀
