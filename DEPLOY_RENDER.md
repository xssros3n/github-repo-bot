# 🎨 Deploy on Render.com - Free & Reliable

## Why Render.com?
- ✅ **FREE** tier available
- ✅ GitHub integration
- ✅ Python support
- ✅ Auto-deploy on push
- ✅ SSL included
- ✅ Very reliable

## 🚀 Step-by-Step Deployment

### Step 1: Push to GitHub

```bash
cd "d:\OneDrive\Desktop\Telegram Bots\github-repo-bot"

# Create repo at https://github.com/new first
git remote add origin https://github.com/YOUR_USERNAME/github-repo-bot.git
git push -u origin main
```

### Step 2: Sign Up on Render

1. Go to https://render.com/
2. Click **"Get Started"**
3. Sign up with GitHub
4. Authorize Render

### Step 3: Create New Web Service

1. Click **"New +"** → **"Background Worker"**
2. Connect your GitHub repository
3. Select `github-repo-bot`
4. Configure:
   - **Name**: `github-repo-bot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python bot_cloud.py`

### Step 4: Add Environment Variables

In the **Environment** section, add:

```
TELEGRAM_BOT_TOKEN=your_bot_token
GITHUB_TOKEN=your_github_token_optional
CLOUD_HOSTING=true
```

### Step 5: Deploy

1. Click **"Create Background Worker"**
2. Wait 3-5 minutes for deployment
3. Check logs for "Bot started successfully"
4. Test in Telegram!

## ✅ Verify

- Status should show "Live"
- Logs should show bot running
- Test `/start` in Telegram

## 🔄 Updates

Push to GitHub and Render auto-deploys:

```bash
git add .
git commit -m "Update"
git push origin main
```

## 💰 Pricing

- **Free Tier**: Perfect for bots
- **Paid Plans**: From $7/month

## 📊 Features

- Real-time logs
- Automatic SSL
- Custom domains
- Health checks
- Metrics

---

**Render.com is excellent for Python bots!** 🎨
