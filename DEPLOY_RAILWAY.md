# 🚂 Deploy on Railway.app - Free & Easy

## Why Railway.app?
- ✅ **FREE** tier (500 hours/month)
- ✅ Direct GitHub deployment
- ✅ Python support
- ✅ Auto-deploy on git push
- ✅ Built-in environment variables
- ✅ Easy to use

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub (Already Done!)

Your code is ready. Just push it:

```bash
cd "d:\OneDrive\Desktop\Telegram Bots\github-repo-bot"

# Create GitHub repo first at https://github.com/new
# Then:
git remote add origin https://github.com/YOUR_USERNAME/github-repo-bot.git
git push -u origin main
```

### Step 2: Sign Up on Railway

1. Go to https://railway.app/
2. Click **"Start a New Project"**
3. Sign up with GitHub (easiest)
4. Authorize Railway to access your repositories

### Step 3: Deploy from GitHub

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository: `github-repo-bot`
4. Railway will automatically detect it's a Python project

### Step 4: Configure Environment Variables

1. Go to your project
2. Click on **"Variables"** tab
3. Add these variables:

```
TELEGRAM_BOT_TOKEN=your_bot_token_from_botfather
GITHUB_TOKEN=your_github_token_optional
CLOUD_HOSTING=true
```

### Step 5: Configure Start Command

1. Go to **"Settings"** tab
2. Find **"Start Command"**
3. Set it to: `python bot_cloud.py`
4. Save

### Step 6: Deploy!

1. Railway will automatically deploy
2. Wait 2-3 minutes
3. Check logs for "Bot started successfully"
4. Test in Telegram!

## ✅ Verify Deployment

1. Check **"Deployments"** tab - should show "Success"
2. Check **"Logs"** - should show "Bot started successfully"
3. Open Telegram and test `/start`

## 🔄 Update Your Bot

Just push to GitHub:

```bash
git add .
git commit -m "Update bot"
git push origin main

# Railway auto-deploys!
```

## 💰 Pricing

- **Free Tier**: 500 hours/month (enough for 1 bot 24/7)
- **Pro Plan**: $5/month (unlimited)

## 📊 Monitoring

Railway provides:
- Real-time logs
- Resource usage
- Deployment history
- Metrics

## 🆘 Troubleshooting

### Bot not starting?
- Check logs in Railway dashboard
- Verify `TELEGRAM_BOT_TOKEN` is set
- Check Python version (should auto-detect)

### Out of free hours?
- Upgrade to Pro ($5/month)
- Or use another free service

---

**Railway.app is perfect for your Python bot!** 🚂
