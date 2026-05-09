# 🚀 Render.com Deployment Guide (Hindi + English)

## 🎯 Why Render.com?

- ✅ **FREE** tier available (750 hours/month)
- ✅ Fast and responsive
- ✅ Auto-deploy from GitHub
- ✅ Python support
- ✅ Environment variables support
- ✅ SSL included
- ✅ No credit card needed for free tier

---

## 📋 Prerequisites / Zarurat

- GitHub account
- Telegram bot token (@BotFather se)
- 10 minutes

---

## 🚀 Step-by-Step Deployment

### Step 1: Push Code to GitHub

```bash
cd "d:\OneDrive\Desktop\Telegram Bots\github-repo-bot"

# Create repo on GitHub first: https://github.com/new
# Repository name: github-repo-bot
# Visibility: Public

# Then push:
git remote add origin https://github.com/YOUR_USERNAME/github-repo-bot.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up on Render.com

1. Go to https://render.com/
2. Click **"Get Started for Free"**
3. Sign up with **GitHub** (easiest option)
4. Authorize Render to access your repositories

### Step 3: Create New Web Service

1. Click **"New +"** button (top right)
2. Select **"Web Service"**
3. Click **"Connect a repository"**
4. Find and select your repository: `github-repo-bot`
5. Click **"Connect"**

### Step 4: Configure Service

Fill in these details:

**Basic Settings:**
- **Name**: `github-repo-bot` (or any name you like)
- **Region**: Select closest to you (Singapore for India)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build & Deploy:**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python bot.py`

**Instance Type:**
- Select **"Free"** plan

### Step 5: Add Environment Variables

Scroll down to **"Environment Variables"** section.

Click **"Add Environment Variable"** and add:

```
Key: TELEGRAM_BOT_TOKEN
Value: your_bot_token_from_botfather
```

**Optional but Recommended:**
```
Key: GITHUB_TOKEN
Value: your_github_personal_access_token
```

```
Key: RATE_LIMIT_REQUESTS
Value: 10
```

```
Key: MAX_FILE_SIZE_MB
Value: 50
```

### Step 6: Deploy!

1. Click **"Create Web Service"** button at bottom
2. Wait 3-5 minutes for deployment
3. Watch the logs - you should see:
   ```
   Bot started successfully!
   Bot is now running and ready to accept requests
   ```

### Step 7: Test Your Bot

1. Open Telegram
2. Search for your bot
3. Send `/start` - Should get welcome message
4. Send a GitHub URL: `https://github.com/octocat/Hello-World`
5. Bot should download and send ZIP file! 🎉

---

## ✅ Verification Checklist

- [ ] Code pushed to GitHub
- [ ] Render.com account created
- [ ] Web Service created
- [ ] Environment variables added
- [ ] Deployment successful (check logs)
- [ ] Bot responds to `/start` in Telegram
- [ ] Bot can download GitHub repositories
- [ ] ZIP file received successfully

---

## 🔄 How to Update Your Bot

Render.com automatically deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Update bot features"
git push origin main

# Render.com will automatically deploy!
# Check deployment status in Render dashboard
```

---

## 📊 Monitoring Your Bot

### Render.com Dashboard

1. Go to https://dashboard.render.com/
2. Click on your service
3. Check:
   - **Logs** - Real-time bot logs
   - **Metrics** - CPU, Memory usage
   - **Events** - Deployment history

### View Logs

In Render dashboard:
- Click on your service
- Go to **"Logs"** tab
- See real-time logs
- Search for errors

---

## 🐛 Troubleshooting

### Bot Not Starting

**Check Logs:**
1. Go to Render dashboard
2. Click on your service
3. Check "Logs" tab

**Common Issues:**
- `TELEGRAM_BOT_TOKEN` not set → Add in Environment Variables
- Wrong Python version → Should auto-detect 3.12
- Dependencies failed → Check requirements.txt

**Fix:**
```
1. Go to Environment tab
2. Verify TELEGRAM_BOT_TOKEN is set correctly
3. Click "Manual Deploy" → "Deploy latest commit"
```

### Bot Responds Slowly

**Solution:**
- Free tier has some limitations
- Upgrade to paid plan ($7/month) for better performance
- Or optimize code (already optimized)

### "Service Unavailable" Error

**Reason:** Free tier services sleep after 15 minutes of inactivity

**Solution:**
- First request after sleep takes 30-60 seconds to wake up
- Upgrade to paid plan for always-on service
- Or use a ping service (not recommended for free tier)

### Deployment Failed

**Check:**
1. Logs for specific error
2. requirements.txt is correct
3. Python version compatibility
4. GitHub repository is accessible

**Fix:**
```
1. Fix the issue in code
2. Push to GitHub
3. Render auto-deploys
```

---

## 💰 Pricing

### Free Tier
- ✅ 750 hours/month (enough for 1 bot)
- ✅ Automatic SSL
- ✅ GitHub auto-deploy
- ⚠️ Sleeps after 15 min inactivity
- ⚠️ Slower cold starts

### Starter Plan ($7/month)
- ✅ Always on (no sleep)
- ✅ Faster performance
- ✅ More resources
- ✅ Better for production

**Recommendation:** Start with free tier, upgrade if needed.

---

## 🎯 Performance Tips

### 1. Keep Bot Active
Free tier sleeps after 15 minutes. First request takes time to wake up.

### 2. Optimize Code
Already done! Bot is optimized for:
- Fast startup
- Efficient memory usage
- Graceful shutdown
- Error handling

### 3. Use GitHub Token
Add `GITHUB_TOKEN` to increase API rate limit from 60 to 5000/hour.

### 4. Monitor Resources
Check Render dashboard for:
- Memory usage
- CPU usage
- Response times

---

## 🔐 Security Best Practices

### 1. Environment Variables
- ✅ Never commit `.env` to GitHub
- ✅ Use Render's Environment Variables
- ✅ Keep tokens secret

### 2. GitHub Token
- ✅ Use Personal Access Token
- ✅ No scopes needed for public repos
- ✅ Rotate tokens periodically

### 3. Monitor Logs
- ✅ Check for suspicious activity
- ✅ Review error logs
- ✅ Track usage patterns

---

## 📈 Scaling Your Bot

### When to Upgrade?

**Indicators:**
- Bot sleeps too often
- Slow response times
- High user count
- Need 24/7 availability

### How to Upgrade?

1. Go to Render dashboard
2. Click on your service
3. Go to **"Settings"**
4. Change **"Instance Type"** to **"Starter"**
5. Click **"Save Changes"**
6. Bot will restart with better resources

---

## 🎓 Advanced Configuration

### Custom Domain (Paid Plans)

1. Go to Settings
2. Add custom domain
3. Configure DNS
4. SSL auto-configured

### Auto-Deploy Settings

1. Settings → Build & Deploy
2. Enable/disable auto-deploy
3. Configure branch
4. Set deploy hooks

### Health Checks

Render automatically monitors your service:
- Checks if bot is running
- Auto-restarts on failure
- Sends notifications

---

## 📞 Support

### Render.com Support
- **Docs**: https://render.com/docs
- **Community**: https://community.render.com/
- **Status**: https://status.render.com/

### Bot Issues
- Check logs in Render dashboard
- Review error messages
- Test locally first

---

## 🎉 Success!

Your bot is now:
- ✅ Live on Render.com
- ✅ Auto-deploying from GitHub
- ✅ Fast and responsive
- ✅ Free (750 hours/month)
- ✅ Production-ready

---

## 🚀 Quick Commands Reference

```bash
# Update bot
git add .
git commit -m "Update"
git push origin main

# View logs locally
tail -f logs/bot_*.log

# Check git status
git status

# Force redeploy on Render
# Go to dashboard → Manual Deploy → Deploy latest commit
```

---

## 💡 Pro Tips

1. ✅ Add GitHub token for better rate limits
2. ✅ Monitor logs regularly
3. ✅ Test locally before pushing
4. ✅ Use meaningful commit messages
5. ✅ Keep dependencies updated
6. ✅ Upgrade to paid plan for production use
7. ✅ Set up notifications in Render
8. ✅ Backup your code regularly

---

## 🎯 Next Steps

1. ✅ Test all features thoroughly
2. ✅ Share bot with users
3. ✅ Monitor performance
4. ✅ Gather feedback
5. ✅ Iterate and improve

---

**Congratulations! Your bot is live on Render.com!** 🎊

**Fast, responsive, and FREE!** 🚀

---

## 📖 Additional Resources

- **Render Docs**: https://render.com/docs/deploy-python
- **Python-telegram-bot**: https://docs.python-telegram-bot.org/
- **GitHub API**: https://docs.github.com/en/rest

---

**Happy Hosting!** 🤖✨
