# 🚀 TeleBotHost Deployment Guide

## 📋 About TeleBotHost

**TeleBotHost** (https://console.telebothost.com/) is a specialized hosting platform for Telegram bots that provides:

- ✅ **Managed Hosting** - No server management needed
- ✅ **24/7 Uptime** - Automatic restarts and monitoring
- ✅ **Easy Deployment** - Git integration or file upload
- ✅ **Scalable** - Automatic resource scaling
- ✅ **Affordable** - Bot-specific pricing
- ✅ **Python Support** - Native Python bot support
- ✅ **Environment Variables** - Secure config management
- ✅ **Logs Access** - Real-time log viewing

## 🎯 Why TeleBotHost is Perfect for This Bot

1. **Specialized for Telegram Bots** - Optimized infrastructure
2. **No Server Management** - Focus on bot, not servers
3. **Automatic Scaling** - Handles traffic spikes
4. **Built-in Monitoring** - Track performance
5. **Easy Updates** - Git push to deploy
6. **Cost-Effective** - Pay only for bot resources

## 📦 Deployment Methods

### Method 1: Git Deployment (Recommended)

#### Step 1: Prepare Repository
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit"

# Push to GitHub/GitLab
git remote add origin <your-repo-url>
git push -u origin main
```

#### Step 2: Connect to TeleBotHost
1. Login to https://console.telebothost.com/
2. Click "Create New Bot"
3. Select "Deploy from Git"
4. Connect your GitHub/GitLab account
5. Select your repository
6. Select branch (main/master)

#### Step 3: Configure Bot
1. Set **Start Command**: `python bot.py`
2. Set **Python Version**: 3.12
3. Add **Environment Variables**:
   ```
   TELEGRAM_BOT_TOKEN=your_token_here
   RATE_LIMIT_REQUESTS=5
   RATE_LIMIT_WINDOW=60
   MAX_FILE_SIZE_MB=50
   DOWNLOAD_TIMEOUT=300
   GITHUB_TOKEN=your_github_token (optional)
   LOG_LEVEL=INFO
   ```

#### Step 4: Deploy
1. Click "Deploy Bot"
2. Wait for deployment (2-5 minutes)
3. Check logs for "Bot started successfully!"
4. Test bot in Telegram

### Method 2: File Upload

#### Step 1: Prepare Files
```bash
# Create deployment package
# Exclude unnecessary files
zip -r bot-deploy.zip . -x "*.git*" "venv/*" "temp/*" "logs/*" "__pycache__/*"
```

#### Step 2: Upload to TeleBotHost
1. Login to https://console.telebothost.com/
2. Click "Create New Bot"
3. Select "Upload Files"
4. Upload bot-deploy.zip
5. Configure as in Method 1

## 🔧 Optimizations for TeleBotHost

### 1. Enhanced Configuration for Cloud Hosting

I'll create an optimized config specifically for TeleBotHost:

**File: `config_cloud.py`** (Enhanced for cloud hosting)
```python
import os
from dotenv import load_dotenv

load_dotenv()

class CloudConfig:
    """Optimized configuration for TeleBotHost"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Rate Limiting (adjusted for cloud)
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 10))  # Increased for cloud
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))
    
    # File Size (optimized for cloud bandwidth)
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Timeouts (adjusted for cloud)
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 180))  # Reduced for faster fails
    
    # GitHub
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    GITHUB_API_BASE = 'https://api.github.com'
    
    # Paths (cloud-optimized)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMP_DIR = os.getenv('TEMP_DIR', os.path.join(BASE_DIR, 'temp'))
    LOGS_DIR = os.getenv('LOGS_DIR', os.path.join(BASE_DIR, 'logs'))
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Cloud-specific settings
    CLOUD_HOSTING = os.getenv('CLOUD_HOSTING', 'true').lower() == 'true'
    MAX_CONCURRENT_DOWNLOADS = int(os.getenv('MAX_CONCURRENT_DOWNLOADS', 5))
    CLEANUP_INTERVAL = int(os.getenv('CLEANUP_INTERVAL', 300))  # 5 minutes
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required in environment variables")
        
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)

config = CloudConfig()
```

### 2. Enhanced Bot for TeleBotHost

**File: `bot_cloud.py`** (Optimized for cloud hosting)
```python
import asyncio
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config_cloud import config
from utils.logger import logger
from utils.cleanup import CleanupManager
from handlers.start_handler import start_command, help_command, stats_command
from handlers.repo_handler import handle_repo_url

# Semaphore for concurrent download limiting
download_semaphore = None

async def error_handler(update: Update, context):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}")
    
    if update and update.effective_message:
        await update.effective_message.reply_text(
            "❌ An error occurred while processing your request.\n"
            "Please try again later."
        )

async def post_init(application: Application):
    """Initialize bot data"""
    global download_semaphore
    download_semaphore = asyncio.Semaphore(config.MAX_CONCURRENT_DOWNLOADS)
    
    application.bot_data['max_size_mb'] = config.MAX_FILE_SIZE_MB
    application.bot_data['download_semaphore'] = download_semaphore
    
    logger.info(f"Bot initialized successfully on TeleBotHost")
    logger.info(f"Max concurrent downloads: {config.MAX_CONCURRENT_DOWNLOADS}")
    
    # Start periodic cleanup task
    asyncio.create_task(periodic_cleanup())

async def post_shutdown(application: Application):
    """Cleanup on shutdown"""
    logger.info("Shutting down bot...")
    CleanupManager.cleanup_old_files(max_age_hours=0)

async def periodic_cleanup():
    """Periodic cleanup of old files"""
    while True:
        try:
            await asyncio.sleep(config.CLEANUP_INTERVAL)
            CleanupManager.cleanup_old_files(max_age_hours=1)
            logger.info("Periodic cleanup completed")
        except Exception as e:
            logger.error(f"Periodic cleanup error: {e}")

def main():
    """Start the bot"""
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated for TeleBotHost")
        
        # Create application
        application = (
            Application.builder()
            .token(config.TELEGRAM_BOT_TOKEN)
            .post_init(post_init)
            .post_shutdown(post_shutdown)
            .concurrent_updates(True)  # Enable concurrent updates
            .build()
        )
        
        # Register handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("stats", stats_command))
        
        # Handle GitHub URLs (text messages)
        application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_repo_url)
        )
        
        # Error handler
        application.add_error_handler(error_handler)
        
        logger.info("Bot started successfully on TeleBotHost!")
        logger.info("Press Ctrl+C to stop")
        
        # Run bot with proper event loop handling
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True  # Drop old updates on restart
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nConfiguration Error: {e}")
        print("Please check your environment variables on TeleBotHost.\n")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal Error: {e}\n")

if __name__ == '__main__':
    # Fix for Python 3.14+ event loop issue on Windows
    if sys.platform == 'win32' and sys.version_info >= (3, 14):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except AttributeError:
            pass
    main()
```

### 3. Enhanced Repository Handler with Concurrency Control

**File: `handlers/repo_handler_cloud.py`**
```python
import os
import time
import asyncio
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.logger import logger
from utils.validators import GitHubValidator
from utils.cleanup import CleanupManager
from services.github_service import GitHubService
from services.telegram_service import TelegramService
from config_cloud import config

# Rate limiting storage
user_requests = {}

def check_rate_limit(user_id: int) -> bool:
    """Check if user exceeded rate limit"""
    current_time = time.time()
    
    if user_id not in user_requests:
        user_requests[user_id] = []
    
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if current_time - req_time < config.RATE_LIMIT_WINDOW
    ]
    
    if len(user_requests[user_id]) >= config.RATE_LIMIT_REQUESTS:
        return False
    
    user_requests[user_id].append(current_time)
    return True

async def handle_repo_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GitHub repository URL with concurrency control"""
    user_id = update.effective_user.id
    message_text = update.message.text.strip()
    
    logger.info(f"User {user_id} sent: {message_text}")
    
    # Rate limiting
    if not check_rate_limit(user_id):
        await TelegramService.send_message(
            update,
            "⚠️ <b>Rate limit exceeded!</b>\n\n"
            f"Please wait before sending another request.\n"
            f"Limit: {config.RATE_LIMIT_REQUESTS} requests per {config.RATE_LIMIT_WINDOW} seconds."
        )
        return
    
    # Validate URL
    is_valid, owner, repo = GitHubValidator.validate_url(message_text)
    
    if not is_valid:
        await TelegramService.send_message(
            update,
            "❌ <b>Invalid GitHub URL</b>\n\n"
            "Please send a valid GitHub repository URL.\n\n"
            "<b>Example:</b>\n"
            "<code>https://github.com/username/repo-name</code>"
        )
        return
    
    # Get semaphore from bot_data
    semaphore = context.bot_data.get('download_semaphore')
    
    # Acquire semaphore for concurrent download control
    async with semaphore:
        await process_download(update, context, owner, repo)

async def process_download(update: Update, context: ContextTypes.DEFAULT_TYPE, owner: str, repo: str):
    """Process the actual download"""
    user_id = update.effective_user.id
    
    # Send processing message
    status_msg = await TelegramService.send_message(
        update,
        "🔍 <b>Checking repository...</b>"
    )
    
    # Initialize services
    github_service = GitHubService()
    
    # Get repository info
    repo_info = await github_service.get_repo_info(owner, repo)
    
    if not repo_info:
        await TelegramService.edit_message(
            status_msg,
            "❌ <b>Repository not found!</b>\n\n"
            "Please check:\n"
            "• Repository exists\n"
            "• Repository is public\n"
            "• URL is correct"
        )
        return
    
    # Check if private
    if github_service.is_private(repo_info):
        await TelegramService.edit_message(
            status_msg,
            "🔒 <b>Private Repository</b>\n\n"
            "Sorry, I can only download public repositories."
        )
        return
    
    # Check size
    repo_size_mb = github_service.get_repo_size_mb(repo_info)
    if repo_size_mb > config.MAX_FILE_SIZE_MB:
        await TelegramService.edit_message(
            status_msg,
            f"📦 <b>Repository too large!</b>\n\n"
            f"Size: {repo_size_mb:.2f} MB\n"
            f"Max allowed: {config.MAX_FILE_SIZE_MB} MB"
        )
        return
    
    # Show repo info
    repo_info_text = TelegramService.format_repo_info(repo_info)
    await TelegramService.edit_message(status_msg, repo_info_text)
    
    # Download repository
    download_msg = await TelegramService.send_message(
        update,
        "⬇️ <b>Downloading repository...</b>"
    )
    
    default_branch = github_service.get_default_branch(repo_info)
    filename = GitHubValidator.sanitize_filename(f"{owner}_{repo}_{default_branch}_{user_id}.zip")
    output_path = os.path.join(config.TEMP_DIR, filename)
    
    success = await github_service.download_repo_zip(owner, repo, default_branch, output_path)
    
    if not success:
        await TelegramService.edit_message(
            download_msg,
            "❌ <b>Download failed!</b>\n\n"
            "Please try again later."
        )
        return
    
    # Send file
    await TelegramService.edit_message(
        download_msg,
        "📤 <b>Uploading to Telegram...</b>"
    )
    
    caption = f"📦 {owner}/{repo}\n🌿 Branch: {default_branch}\n☁️ Hosted on TeleBotHost"
    file_sent = await TelegramService.send_document(update, output_path, caption)
    
    if file_sent:
        await TelegramService.edit_message(
            download_msg,
            "✅ <b>Done!</b>"
        )
        
        # Update user stats
        context.user_data['total_downloads'] = context.user_data.get('total_downloads', 0) + 1
        
        logger.info(f"Successfully sent {owner}/{repo} to user {user_id}")
    else:
        await TelegramService.edit_message(
            download_msg,
            "❌ <b>Failed to send file!</b>\n\n"
            "The file might be too large for Telegram."
        )
    
    # Cleanup
    CleanupManager.delete_file(output_path)
```

## 📝 Required Files for TeleBotHost

### 1. Create `requirements.txt` (Already exists, but verify)
```txt
python-telegram-bot==21.0.1
requests==2.31.0
python-dotenv==1.0.1
aiohttp==3.9.3
aiofiles==23.2.1
```

### 2. Create `runtime.txt` (Specify Python version)
```txt
python-3.12
```

### 3. Create `Procfile` (Optional, for process management)
```txt
worker: python bot.py
```

### 4. Create `.telebothost.yml` (TeleBotHost configuration)
```yaml
name: github-repo-downloader
runtime: python-3.12
start_command: python bot.py

environment:
  TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
  RATE_LIMIT_REQUESTS: 10
  RATE_LIMIT_WINDOW: 60
  MAX_FILE_SIZE_MB: 50
  DOWNLOAD_TIMEOUT: 180
  GITHUB_TOKEN: ${GITHUB_TOKEN}
  LOG_LEVEL: INFO
  CLOUD_HOSTING: true
  MAX_CONCURRENT_DOWNLOADS: 5
  CLEANUP_INTERVAL: 300

resources:
  memory: 512MB
  cpu: 1

health_check:
  enabled: true
  interval: 60
  timeout: 10

auto_restart:
  enabled: true
  max_restarts: 5

logging:
  level: INFO
  retention_days: 7
```

## 🚀 Step-by-Step Deployment to TeleBotHost

### Step 1: Sign Up
1. Go to https://console.telebothost.com/
2. Click "Sign Up" or "Get Started"
3. Create account with email
4. Verify email

### Step 2: Create New Bot Project
1. Click "Create New Bot"
2. Enter bot name: "GitHub Repo Downloader"
3. Select deployment method: "Git Repository" or "File Upload"

### Step 3: Configure Environment Variables
In TeleBotHost dashboard, add these environment variables:

```
TELEGRAM_BOT_TOKEN = your_bot_token_from_botfather
GITHUB_TOKEN = your_github_token (optional but recommended)
RATE_LIMIT_REQUESTS = 10
MAX_FILE_SIZE_MB = 50
LOG_LEVEL = INFO
CLOUD_HOSTING = true
```

### Step 4: Deploy
1. If using Git: Connect repository and click "Deploy"
2. If using Upload: Upload ZIP file and click "Deploy"
3. Wait for deployment (2-5 minutes)

### Step 5: Monitor
1. Check "Logs" tab for "Bot started successfully!"
2. Check "Status" tab for uptime
3. Test bot in Telegram

### Step 6: Configure Auto-Scaling (Optional)
1. Go to "Settings" > "Scaling"
2. Enable auto-scaling
3. Set min/max instances
4. Set CPU/Memory thresholds

## 📊 TeleBotHost Dashboard Features

### Monitoring
- **Real-time Logs** - View bot logs live
- **Performance Metrics** - CPU, Memory, Network usage
- **Error Tracking** - Track and analyze errors
- **Uptime Monitoring** - 99.9% uptime guarantee

### Management
- **Auto Restart** - Automatic restart on crashes
- **Auto Scaling** - Scale based on load
- **Environment Variables** - Secure config management
- **Git Integration** - Deploy on push

### Analytics
- **User Statistics** - Track active users
- **Request Metrics** - Monitor request rates
- **Error Rates** - Track error frequency
- **Response Times** - Monitor performance

## 💰 Pricing Considerations

TeleBotHost typically offers:
- **Free Tier** - Limited resources, good for testing
- **Basic Plan** - $5-10/month, suitable for small bots
- **Pro Plan** - $20-30/month, for production bots
- **Enterprise** - Custom pricing for high-traffic bots

**Recommendation for this bot:** Start with Basic Plan, upgrade if needed.

## 🔧 Optimization Tips for TeleBotHost

### 1. Enable Concurrent Updates
Already implemented in `bot_cloud.py`:
```python
.concurrent_updates(True)
```

### 2. Implement Download Queue
Use semaphore to limit concurrent downloads:
```python
download_semaphore = asyncio.Semaphore(5)
```

### 3. Aggressive Cleanup
Periodic cleanup every 5 minutes:
```python
CLEANUP_INTERVAL = 300
```

### 4. Optimize File Sizes
Reduce max file size for faster transfers:
```python
MAX_FILE_SIZE_MB = 50
```

### 5. Use GitHub Token
Always use GitHub token to avoid rate limits:
```python
GITHUB_TOKEN = your_token
```

## 📈 Scaling Strategy

### Vertical Scaling (Increase Resources)
1. Go to TeleBotHost dashboard
2. Settings > Resources
3. Increase Memory/CPU
4. Apply changes

### Horizontal Scaling (Multiple Instances)
1. Settings > Scaling
2. Enable auto-scaling
3. Set min instances: 1
4. Set max instances: 3-5
5. Set scale triggers

## 🔍 Monitoring & Alerts

### Set Up Alerts
1. Dashboard > Alerts
2. Create alert for:
   - High error rate (> 5%)
   - High memory usage (> 80%)
   - Bot offline
   - Slow response time (> 5s)

### Log Analysis
1. Dashboard > Logs
2. Filter by level (ERROR, WARNING)
3. Set up log exports
4. Integrate with external tools

## 🐛 Troubleshooting on TeleBotHost

### Bot Not Starting
1. Check logs for errors
2. Verify TELEGRAM_BOT_TOKEN is set
3. Check Python version (3.12)
4. Verify requirements.txt

### High Memory Usage
1. Reduce MAX_CONCURRENT_DOWNLOADS
2. Reduce MAX_FILE_SIZE_MB
3. Increase cleanup frequency
4. Upgrade plan

### Slow Performance
1. Enable concurrent updates
2. Optimize download logic
3. Use CDN for popular repos
4. Upgrade resources

## ✅ Post-Deployment Checklist

- [ ] Bot deployed successfully
- [ ] Environment variables configured
- [ ] Bot responds to /start
- [ ] Can download test repository
- [ ] Logs are accessible
- [ ] Monitoring enabled
- [ ] Alerts configured
- [ ] Auto-restart enabled
- [ ] Backup strategy in place
- [ ] Documentation updated

## 🎯 Next Steps After Deployment

1. **Monitor for 24 hours** - Check logs and performance
2. **Test with real users** - Invite beta testers
3. **Optimize based on metrics** - Adjust settings
4. **Set up alerts** - Get notified of issues
5. **Plan for scaling** - Prepare for growth

## 📞 TeleBotHost Support

- **Documentation**: https://docs.telebothost.com/
- **Support Email**: support@telebothost.com
- **Community**: Discord/Telegram group
- **Status Page**: status.telebothost.com

---

**Your bot is now optimized and ready for TeleBotHost deployment!** 🚀
