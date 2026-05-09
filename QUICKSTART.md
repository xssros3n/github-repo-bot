# ⚡ Quick Start - Deploy in 10 Minutes

## 🎯 3 Simple Steps

### 1️⃣ Push to GitHub (2 minutes)

```bash
cd "d:\OneDrive\Desktop\Telegram Bots\github-repo-bot"

# Create repo at https://github.com/new first
git remote add origin https://github.com/YOUR_USERNAME/github-repo-bot.git
git push -u origin main
```

### 2️⃣ Deploy on Render (5 minutes)

1. Go to https://render.com/
2. Sign up with GitHub
3. New + → Web Service
4. Connect your repository
5. Settings:
   - Build: `pip install -r requirements.txt`
   - Start: `python bot.py`
   - Plan: **Free**
6. Add Environment Variable:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   ```
7. Click **"Create Web Service"**

### 3️⃣ Test (3 minutes)

1. Wait for deployment (check logs)
2. Open Telegram
3. Send `/start` to your bot
4. Send: `https://github.com/octocat/Hello-World`
5. Receive ZIP file! 🎉

---

## ✅ Done!

Your bot is live and running on Render.com!

**Full Guide:** Read `RENDER_DEPLOYMENT.md`

---

## 🔄 Update Bot

```bash
git add .
git commit -m "Update"
git push origin main
# Render auto-deploys!
```

---

## 💡 Important

- **Free tier**: 750 hours/month
- **Sleeps**: After 15 min inactivity
- **First request**: Takes 30-60 sec to wake up
- **Upgrade**: $7/month for always-on

---

**Fast, Free, and Easy!** 🚀
