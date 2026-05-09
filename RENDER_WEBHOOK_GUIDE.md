# 🚀 Render.com Deployment Guide - Webhook Version

## 📋 Overview

This bot is now configured to run on **Render.com free tier** using **webhooks** instead of polling. This makes it:
- ✅ **Free** - No cost on Render free tier
- ✅ **Fast** - Instant response via webhooks
- ✅ **Scalable** - No polling overhead
- ✅ **Production-ready** - Proper error handling and logging

---

## 🎯 Architecture Changes

### Before (Polling):
```
Bot → Telegram API (every few seconds)
❌ Constant polling
❌ Resource intensive
❌ Not suitable for free tier
```

### After (Webhook):
```
Telegram → Your Render App → Bot
✅ Event-driven
✅ Resource efficient
✅ Perfect for free tier
```

---

## 📦 Prerequisites

1. **GitHub Account** - To host your code
2. **Render Account** - Sign up at https://render.com (free)
3. **Telegram Bot Token** - From @BotFather
4. **GitHub Token** (optional) - For higher API rate limits

---

## 🚀 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
cd github-repo-bot

# If not already initialized
git init
git add .
git commit -m "Webhook version for Render deployment"

# Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/github-repo-bot.git
git branch -M main
git push -u origin main
```

### Step 2: Create Render Web Service

1. Go to https://dashboard.render.com/
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select `github-repo-bot` repository

### Step 3: Configure Service

**Basic Settings:**
- **Name**: `github-repo-bot` (or any name)
- **Region**: Choose closest to you
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --worker-class gthread`

**Instance Type:**
- Select **"Free"**

### Step 4: Add Environment Variables

Click **"Add Environment Variable"** for each:

#### Required Variables:

```
Key: TELEGRAM_BOT_TOKEN
Value: your_bot_token_from_botfather
```

```
Key: WEBHOOK_URL
Value: https://your-app-name.onrender.com
```

**Important:** Replace `your-app-name` with your actual Render app name!

#### Optional but Recommended:

```
Key: GITHUB_TOKEN
Value: your_github_personal_access_token
```

```
Key: MAX_FILE_SIZE_MB
Value: 50
```

```
Key: RATE_LIMIT_REQUESTS
Value: 5
```

```
Key: LOG_LEVEL
Value: INFO
```

### Step 5: Deploy

1. Click **"Create Web Service"**
2. Wait 3-5 minutes for deployment
3. Watch the logs for:
   ```
   Bot initialized successfully
   Webhook set successfully
   ```

### Step 6: Verify Deployment

#### Check Health Endpoint:
Visit: `https://your-app-name.onrender.com/`

Should return:
```json
{
  "status": "ok",
  "message": "GitHub Repository Downloader Bot is running",
  "webhook_configured": true
}
```

#### Check Webhook Info:
Visit: `https://your-app-name.onrender.com/webhook_info`

Should show webhook details.

#### Test in Telegram:
1. Open your bot in Telegram
2. Send `/start`
3. Send a GitHub URL: `https://github.com/octocat/Hello-World`
4. Bot should respond instantly!

---

## 🔧 Configuration Details

### Environment Variables Explained

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | ✅ Yes | - | Your bot token from @BotFather |
| `WEBHOOK_URL` | ✅ Yes | - | Your Render app URL |
| `GITHUB_TOKEN` | ❌ No | - | GitHub token for higher rate limits |
| `MAX_FILE_SIZE_MB` | ❌ No | 50 | Maximum repository size |
| `RATE_LIMIT_REQUESTS` | ❌ No | 5 | Max requests per time window |
| `RATE_LIMIT_WINDOW` | ❌ No | 60 | Time window in seconds |
| `DOWNLOAD_TIMEOUT` | ❌ No | 300 | Download timeout in seconds |
| `LOG_LEVEL` | ❌ No | INFO | Logging level |
| `ENVIRONMENT` | ❌ No | production | Environment mode |

### Getting Your Webhook URL

Your webhook URL format:
```
https://YOUR-APP-NAME.onrender.com
```

Example:
```
https://github-repo-bot-abc123.onrender.com
```

**Find it in:**
- Render Dashboard → Your Service → Settings → URL

---

## 🔍 Monitoring & Debugging

### View Logs

In Render Dashboard:
1. Go to your service
2. Click **"Logs"** tab
3. See real-time logs

### Check Webhook Status

Visit: `https://your-app.onrender.com/webhook_info`

Returns:
```json
{
  "ok": true,
  "url": "https://your-app.onrender.com/YOUR_BOT_TOKEN",
  "pending_update_count": 0,
  "last_error_message": null
}
```

### Manual Webhook Setup

If webhook fails, visit:
`https://your-app.onrender.com/set_webhook`

This will manually configure the webhook.

---

## 🐛 Troubleshooting

### Bot Not Responding

**Check 1: Webhook Status**
```
Visit: https://your-app.onrender.com/webhook_info
```

**Check 2: Logs**
- Go to Render Dashboard → Logs
- Look for errors

**Check 3: Environment Variables**
- Verify `TELEGRAM_BOT_TOKEN` is correct
- Verify `WEBHOOK_URL` matches your Render URL

**Fix:**
```
1. Go to Render Dashboard
2. Environment → Edit WEBHOOK_URL
3. Save and redeploy
```

### Webhook Not Set

**Symptoms:**
- Bot doesn't respond
- `/webhook_info` shows empty URL

**Solution:**
```
Visit: https://your-app.onrender.com/set_webhook
```

This manually sets the webhook.

### "Application Error" on Render

**Check Logs for:**
- Missing environment variables
- Import errors
- Configuration errors

**Common Fixes:**
1. Verify all required env vars are set
2. Check `requirements.txt` is correct
3. Ensure `app.py` exists
4. Redeploy

### Rate Limit Errors

**Symptoms:**
- "Too many requests" errors
- Slow responses

**Solution:**
Add `GITHUB_TOKEN` environment variable:
```
Key: GITHUB_TOKEN
Value: your_github_token
```

This increases GitHub API limit from 60 to 5000/hour.

### File Upload Fails

**Symptoms:**
- "Failed to send file" error
- Large repositories fail

**Solutions:**
1. Reduce `MAX_FILE_SIZE_MB`:
   ```
   MAX_FILE_SIZE_MB=30
   ```

2. Add GitHub token for better performance

3. Check Telegram file size limits (50MB for bots)

---

## 🔄 Updating Your Bot

### Automatic Deployment

Render auto-deploys on git push:

```bash
# Make changes
git add .
git commit -m "Update bot"
git push origin main

# Render automatically deploys!
```

### Manual Deployment

In Render Dashboard:
1. Go to your service
2. Click **"Manual Deploy"**
3. Select **"Deploy latest commit"**

---

## 💰 Render Free Tier Limits

### What's Included:
- ✅ 750 hours/month (enough for 1 bot 24/7)
- ✅ Automatic SSL
- ✅ Custom domains
- ✅ Auto-deploy from GitHub

### Limitations:
- ⚠️ Spins down after 15 minutes of inactivity
- ⚠️ First request after sleep takes 30-60 seconds
- ⚠️ 512MB RAM
- ⚠️ Shared CPU

### Upgrade Options:
- **Starter Plan**: $7/month
  - Always on (no sleep)
  - Faster performance
  - More resources

---

## 🎯 Performance Optimization

### Already Implemented:
- ✅ Webhook instead of polling
- ✅ Async operations
- ✅ Efficient file handling
- ✅ Automatic cleanup
- ✅ Rate limiting
- ✅ Error handling

### Additional Tips:
1. **Add GitHub Token** - Increases API rate limit
2. **Monitor Logs** - Check for errors regularly
3. **Adjust Rate Limits** - Based on usage
4. **Clean Temp Files** - Automatic cleanup enabled

---

## 🔐 Security Best Practices

### Implemented:
- ✅ Environment variables for secrets
- ✅ Input validation
- ✅ Rate limiting
- ✅ Filename sanitization
- ✅ Public repos only
- ✅ File size limits

### Additional Recommendations:
1. **Rotate Tokens** - Change tokens periodically
2. **Monitor Usage** - Check logs for suspicious activity
3. **Update Dependencies** - Keep packages updated
4. **Backup Code** - Keep GitHub repo updated

---

## 📊 Monitoring Checklist

### Daily:
- [ ] Check bot responds in Telegram
- [ ] Verify webhook status
- [ ] Review error logs

### Weekly:
- [ ] Check Render dashboard metrics
- [ ] Review usage statistics
- [ ] Update dependencies if needed

### Monthly:
- [ ] Rotate tokens
- [ ] Review and optimize settings
- [ ] Check for updates

---

## 🆘 Getting Help

### Resources:
- **Render Docs**: https://render.com/docs
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **GitHub Issues**: Report bugs in your repo

### Common Issues:
1. **Bot not responding** → Check webhook status
2. **Slow responses** → Check Render logs
3. **File upload fails** → Check file size limits
4. **Rate limit errors** → Add GitHub token

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web Service created
- [ ] `TELEGRAM_BOT_TOKEN` added
- [ ] `WEBHOOK_URL` added (correct format)
- [ ] `GITHUB_TOKEN` added (optional)
- [ ] Service deployed successfully
- [ ] Health check returns OK
- [ ] Webhook info shows correct URL
- [ ] Bot responds to `/start`
- [ ] Bot can download repositories
- [ ] Logs show no errors

---

## 🎉 Success!

Your bot is now:
- ✅ Running on Render free tier
- ✅ Using webhooks (fast & efficient)
- ✅ Production-ready
- ✅ Auto-deploying from GitHub
- ✅ Properly monitored

**Test it:** Send `/start` to your bot in Telegram!

---

## 📝 Quick Reference

### Important URLs:
```
Health Check: https://your-app.onrender.com/
Webhook Info: https://your-app.onrender.com/webhook_info
Set Webhook: https://your-app.onrender.com/set_webhook
```

### Important Commands:
```bash
# Update bot
git add .
git commit -m "Update"
git push origin main

# View logs
# Go to Render Dashboard → Logs

# Redeploy
# Render Dashboard → Manual Deploy
```

---

**Happy Hosting!** 🚀
