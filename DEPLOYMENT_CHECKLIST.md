# ✅ Render.com Deployment Checklist

## 🎯 Pre-Deployment

- [x] Code converted to webhook architecture
- [x] Flask app created (`app.py`)
- [x] Configuration updated (`config.py`)
- [x] Dependencies updated (`requirements.txt`)
- [x] Render config created (`render.yaml`)
- [x] Environment template created (`.env.example`)
- [x] Documentation created
- [x] Code pushed to GitHub

## 🚀 Deployment Steps

### 1. Render Account Setup
- [ ] Go to https://render.com/
- [ ] Sign up with GitHub
- [ ] Authorize Render to access repositories

### 2. Create Web Service
- [ ] Click "New +" → "Web Service"
- [ ] Connect repository: `github-repo-bot`
- [ ] Select branch: `main`

### 3. Configure Service

**Basic Settings:**
- [ ] Name: `github-repo-bot` (or your choice)
- [ ] Region: Select closest to you
- [ ] Branch: `main`
- [ ] Runtime: `Python 3`

**Build & Deploy:**
- [ ] Build Command: `pip install -r requirements.txt`
- [ ] Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --worker-class gthread`

**Instance Type:**
- [ ] Select: **Free**

### 4. Environment Variables

**Required:**
- [ ] `TELEGRAM_BOT_TOKEN` = `your_bot_token`
- [ ] `WEBHOOK_URL` = `https://your-app-name.onrender.com`

**Optional but Recommended:**
- [ ] `GITHUB_TOKEN` = `your_github_token`
- [ ] `MAX_FILE_SIZE_MB` = `50`
- [ ] `RATE_LIMIT_REQUESTS` = `5`
- [ ] `LOG_LEVEL` = `INFO`

### 5. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait 3-5 minutes for deployment
- [ ] Watch logs for success messages

## ✅ Post-Deployment Verification

### 1. Health Check
- [ ] Visit: `https://your-app-name.onrender.com/`
- [ ] Should return: `{"status": "ok", ...}`

### 2. Webhook Status
- [ ] Visit: `https://your-app-name.onrender.com/webhook_info`
- [ ] Verify webhook URL is set correctly
- [ ] Check `pending_update_count` is 0
- [ ] Verify no error messages

### 3. Telegram Test
- [ ] Open bot in Telegram
- [ ] Send `/start` → Should get welcome message
- [ ] Send `/help` → Should get help message
- [ ] Send `/stats` → Should get statistics
- [ ] Send GitHub URL: `https://github.com/octocat/Hello-World`
- [ ] Should receive ZIP file

### 4. Logs Check
- [ ] Go to Render Dashboard → Logs
- [ ] Verify no errors
- [ ] Check for "Bot initialized successfully"
- [ ] Check for "Webhook set successfully"

## 🐛 Troubleshooting

### If Bot Doesn't Respond:

**Step 1: Check Webhook**
```
Visit: https://your-app-name.onrender.com/webhook_info
```

**Step 2: Manual Webhook Setup**
```
Visit: https://your-app-name.onrender.com/set_webhook
```

**Step 3: Check Logs**
- Render Dashboard → Logs
- Look for errors

**Step 4: Verify Environment Variables**
- `TELEGRAM_BOT_TOKEN` is correct
- `WEBHOOK_URL` matches your Render URL (no trailing slash)

### If Webhook Setup Fails:

**Check:**
- [ ] `WEBHOOK_URL` format: `https://your-app.onrender.com` (no trailing slash)
- [ ] `TELEGRAM_BOT_TOKEN` is valid
- [ ] App is running (check health endpoint)

**Fix:**
1. Update `WEBHOOK_URL` in Render environment variables
2. Save changes
3. Redeploy
4. Visit `/set_webhook` endpoint

## 📊 Monitoring

### Daily Checks:
- [ ] Bot responds in Telegram
- [ ] No errors in Render logs
- [ ] Webhook status is OK

### Weekly Checks:
- [ ] Review Render metrics
- [ ] Check for any rate limit issues
- [ ] Verify temp files are cleaned up

## 🔄 Updates

### To Update Bot:
```bash
git add .
git commit -m "Update bot"
git push origin main
# Render auto-deploys!
```

### Manual Redeploy:
- Render Dashboard → Manual Deploy → Deploy latest commit

## 💡 Pro Tips

1. **Add GitHub Token** - Increases API rate limit from 60 to 5000/hour
2. **Monitor Logs** - Check regularly for errors
3. **Test Locally First** - Before pushing to production
4. **Keep Tokens Secret** - Never commit to GitHub
5. **Backup Configuration** - Save environment variables

## 🎉 Success Criteria

Your deployment is successful when:
- ✅ Health check returns OK
- ✅ Webhook info shows correct URL
- ✅ Bot responds to `/start`
- ✅ Bot can download repositories
- ✅ No errors in logs
- ✅ Files are sent successfully

## 📞 Need Help?

- **Documentation**: [RENDER_WEBHOOK_GUIDE.md](RENDER_WEBHOOK_GUIDE.md)
- **Migration Guide**: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- **Render Docs**: https://render.com/docs
- **GitHub Issues**: Report problems in your repo

---

## 🎯 Quick Reference

### Important URLs:
```
Your App: https://your-app-name.onrender.com
Health Check: https://your-app-name.onrender.com/
Webhook Info: https://your-app-name.onrender.com/webhook_info
Set Webhook: https://your-app-name.onrender.com/set_webhook
```

### Environment Variables:
```
TELEGRAM_BOT_TOKEN=your_token
WEBHOOK_URL=https://your-app-name.onrender.com
GITHUB_TOKEN=your_github_token (optional)
```

### Commands:
```bash
# Update bot
git push origin main

# View logs
# Render Dashboard → Logs

# Redeploy
# Render Dashboard → Manual Deploy
```

---

**Your bot is ready for production!** 🚀
