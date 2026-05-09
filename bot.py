import asyncio
import sys
import signal
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import config
from utils.logger import logger
from utils.cleanup import CleanupManager
from handlers.start_handler import start_command, help_command, stats_command
from handlers.repo_handler import handle_repo_url

# Global flag for graceful shutdown
shutdown_flag = False

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
    application.bot_data['max_size_mb'] = config.MAX_FILE_SIZE_MB
    logger.info("Bot initialized successfully")

async def post_shutdown(application: Application):
    """Cleanup on shutdown"""
    logger.info("Shutting down bot...")
    CleanupManager.cleanup_old_files(max_age_hours=0)
    logger.info("Cleanup completed")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    global shutdown_flag
    shutdown_flag = True
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")

def main():
    """Start the bot"""
    try:
        # Register signal handlers for graceful shutdown
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)
        
        # Validate configuration
        config.validate()
        logger.info("Configuration validated")
        logger.info("Starting GitHub Repository Downloader Bot...")
        
        # Create application
        application = (
            Application.builder()
            .token(config.TELEGRAM_BOT_TOKEN)
            .post_init(post_init)
            .post_shutdown(post_shutdown)
            .connect_timeout(30)
            .read_timeout(30)
            .write_timeout(30)
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
        
        logger.info("Bot started successfully!")
        logger.info("Bot is now running and ready to accept requests")
        logger.info("Press Ctrl+C to stop")
        
        # Run bot with proper event loop handling
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run with optimized settings for Render.com
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nConfiguration Error: {e}")
        print("Please check your .env file and ensure TELEGRAM_BOT_TOKEN is set.\n")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nFatal Error: {e}\n")

if __name__ == '__main__':
    # Fix for Python 3.14+ event loop issue on Windows
    if sys.platform == 'win32' and sys.version_info >= (3, 14):
        try:
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        except AttributeError:
            pass  # Policy not available in this Python version
    main()
