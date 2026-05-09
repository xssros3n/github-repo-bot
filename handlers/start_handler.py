from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.logger import logger

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started the bot")
    
    welcome_message = (
        f"👋 <b>Welcome {user.first_name}!</b>\n\n"
        "🤖 I'm a GitHub Repository Downloader Bot.\n\n"
        "<b>How to use:</b>\n"
        "1️⃣ Send me any public GitHub repository URL\n"
        "2️⃣ I'll download it and send you a ZIP file\n\n"
        "<b>Example:</b>\n"
        "<code>https://github.com/username/repo-name</code>\n\n"
        "📌 <b>Commands:</b>\n"
        "/start - Show this message\n"
        "/help - Get help\n"
        "/stats - View bot statistics\n\n"
        "⚠️ <b>Note:</b> Only public repositories are supported."
    )
    
    await update.message.reply_text(welcome_message, parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    logger.info(f"User {update.effective_user.id} requested help")
    
    help_message = (
        "📖 <b>Help - GitHub Repo Downloader</b>\n\n"
        "<b>Supported URL formats:</b>\n"
        "• https://github.com/owner/repo\n"
        "• https://github.com/owner/repo.git\n"
        "• http://github.com/owner/repo\n\n"
        "<b>Features:</b>\n"
        "✅ Automatic branch detection\n"
        "✅ Repository information preview\n"
        "✅ Fast downloads\n"
        "✅ File size validation\n\n"
        "<b>Limitations:</b>\n"
        f"• Max file size: {context.bot_data.get('max_size_mb', 50)} MB\n"
        "• Public repositories only\n"
        "• Rate limit: 5 requests per minute\n\n"
        "<b>Need help?</b>\n"
        "Contact: @YourSupportUsername"
    )
    
    await update.message.reply_text(help_message, parse_mode=ParseMode.HTML)

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command"""
    user_id = update.effective_user.id
    logger.info(f"User {user_id} requested stats")
    
    user_data = context.user_data
    downloads = user_data.get('total_downloads', 0)
    
    stats_message = (
        "📊 <b>Your Statistics</b>\n\n"
        f"📥 Total Downloads: {downloads}\n"
        f"👤 User ID: <code>{user_id}</code>\n\n"
        "Keep using the bot to increase your stats! 🚀"
    )
    
    await update.message.reply_text(stats_message, parse_mode=ParseMode.HTML)
