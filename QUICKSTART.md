# ⚡ Quick Start (5 Minutes)

## Prerequisites
- Python 3.12+ installed
- Telegram account

## Steps

### 1. Get Bot Token (2 minutes)
1. Open Telegram → Search `@BotFather`
2. Send: `/newbot`
3. Follow instructions
4. Copy the token (looks like: `1234567890:ABCdef...`)

### 2. Setup Bot (2 minutes)

**Windows:**
```bash
# Navigate to project folder
cd github-repo-bot

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure
copy .env.example .env
notepad .env
# Paste your token, save and close
```

**Linux/macOS:**
```bash
# Navigate to project folder
cd github-repo-bot

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
nano .env
# Paste your token, save (Ctrl+X, Y, Enter)
```

### 3. Run Bot (1 minute)

```bash
python bot.py
```

You should see:
```
Bot started successfully!
Press Ctrl+C to stop
```

### 4. Test Bot

1. Open Telegram
2. Search for your bot
3. Send: `/start`
4. Send: `https://github.com/octocat/Hello-World`
5. Receive ZIP file! 🎉

## That's It! 🚀

Your bot is now running!

### Next Steps:
- Read [README.md](README.md) for full documentation
- Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for deployment
- Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the code

### Common Issues:

**"TELEGRAM_BOT_TOKEN is required"**
→ Edit `.env` and add your token

**"No module named 'telegram'"**
→ Run: `pip install -r requirements.txt`

**Bot doesn't respond**
→ Check if bot is running
→ Verify token is correct

### Stop Bot:
Press `Ctrl+C` in terminal

### Run Again:
```bash
# Windows
venv\Scripts\activate
python bot.py

# Linux/macOS
source venv/bin/activate
python bot.py
```

---

Need help? Check [SETUP_GUIDE.md](SETUP_GUIDE.md)
