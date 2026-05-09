import asyncio
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config_cloud import config
from utils.logger import logger
from utils.cleanup import CleanupManager
from handlers.start_handler import start_command, help_command, stats_command
from handlers.repo_handler import handle_repo_url

# Global semaphore for concurrent download limiting
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
    
    if config.CLOUD_HOSTING:
        logger.info(f"Bot initialized on TeleBotHost")
        logger.info(f"Max concurrent downloads: {config.MAX_CONCURRENT_DOWNLOADS}")
        logger.info(f"Cleanup interval: {config.CLEANUP_INTERVAL}s")
    else:
        logger.info("Bot initialized successfully")
    
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
            deleted = CleanupManager.cleanup_old_files(max_age_hours=1)
            if deleted > 0:
                logger.info(f"Periodic cleanup: removed {deleted} files")
        except Exception as e:
            logger.error(f"Periodic cleanup error: {e}")

def main():
    """Start the bot"""
    try:
        # Validate configuration
        config.validate()
        logger.info("Configuration validated")
        
        # Create application with cloud optimizations
        builder = Application.builder().token(config.TELEGRAM_BOT_TOKEN)
        
        # Enable concurrent updates for better performance
        if config.CLOUD_HOSTING:
            builder = builder.concurrent_updates(True)
            logger.info("Concurrent updates enabled")
        
        application = (
            builder
            .post_init(post_init)
            .post_shutdown(post_shutdown)
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
        
        if config.CLOUD_HOSTING:
            logger.info("Bot started successfully on TeleBotHost!")
        else:
            logger.info("Bot started successfully!")
        
        logger.info("Press Ctrl+C to stop")
        
        # Run bot with proper event loop handling
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Run with cloud optimizations
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True if config.CLOUD_HOSTING else False
        )
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        print(f"\nConfiguration Error: {e}")
        print("Please check your environment variables.\n")
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
