"""
GitHub Repository Downloader Bot - Webhook Version
Optimized for Render.com free tier deployment
"""

import os
import asyncio
from threading import Thread
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import config
from utils.logger import logger
from utils.cleanup import CleanupManager
from handlers.start_handler import start_command, help_command, stats_command
from handlers.repo_handler import handle_repo_url

# Initialize Flask app
app = Flask(__name__)

# Global bot application
bot_app = None
event_loop = None


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors"""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)
    
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request.\n"
                "Please try again later."
            )
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")


async def post_init(application: Application):
    """Initialize bot data"""
    application.bot_data['max_size_mb'] = config.MAX_FILE_SIZE_MB
    logger.info("Bot initialized successfully")
    
    # Set webhook
    webhook_url = f"{config.WEBHOOK_URL}/{config.TELEGRAM_BOT_TOKEN}"
    try:
        await application.bot.set_webhook(
            url=webhook_url,
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        logger.info(f"Webhook set successfully: {webhook_url}")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")
        raise


async def post_shutdown(application: Application):
    """Cleanup on shutdown"""
    logger.info("Shutting down bot...")
    try:
        await application.bot.delete_webhook()
        logger.info("Webhook deleted")
    except Exception as e:
        logger.error(f"Error deleting webhook: {e}")
    
    CleanupManager.cleanup_old_files(max_age_hours=0)
    logger.info("Cleanup completed")


def create_application():
    """Create and configure the bot application"""
    logger.info("Creating bot application...")
    
    # Validate configuration
    config.validate()
    logger.info("Configuration validated")
    
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
    
    logger.info("Bot application created successfully")
    return application


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return "Bot is running", 200


@app.route(f'/{config.TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    """Handle incoming webhook updates from Telegram"""
    try:
        # Get update from request
        update_data = request.get_json(force=True)
        
        # Create Update object
        update = Update.de_json(update_data, bot_app.bot)
        
        # Process update asynchronously
        asyncio.run_coroutine_threadsafe(
            bot_app.process_update(update),
            event_loop
        )
        
        return jsonify({'ok': True}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/set_webhook', methods=['GET'])
def set_webhook_endpoint():
    """Manually trigger webhook setup (for debugging)"""
    try:
        webhook_url = f"{config.WEBHOOK_URL}/{config.TELEGRAM_BOT_TOKEN}"
        
        async def _set_webhook():
            await bot_app.bot.set_webhook(
                url=webhook_url,
                allowed_updates=Update.ALL_TYPES,
                drop_pending_updates=True
            )
        
        future = asyncio.run_coroutine_threadsafe(_set_webhook(), event_loop)
        future.result(timeout=10)
        
        return jsonify({
            'ok': True,
            'message': 'Webhook set successfully',
            'webhook_url': webhook_url
        }), 200
    except Exception as e:
        logger.error(f"Error setting webhook: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500


@app.route('/webhook_info', methods=['GET'])
def webhook_info():
    """Get current webhook information"""
    try:
        async def _get_info():
            return await bot_app.bot.get_webhook_info()
        
        future = asyncio.run_coroutine_threadsafe(_get_info(), event_loop)
        info = future.result(timeout=10)
        
        return jsonify({
            'ok': True,
            'url': info.url,
            'has_custom_certificate': info.has_custom_certificate,
            'pending_update_count': info.pending_update_count,
            'last_error_date': info.last_error_date,
            'last_error_message': info.last_error_message,
            'max_connections': info.max_connections,
            'allowed_updates': info.allowed_updates
        }), 200
    except Exception as e:
        logger.error(f"Error getting webhook info: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500


def run_async_loop():
    """Run the asyncio event loop in a separate thread"""
    global event_loop
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_forever()


def initialize_bot():
    """Initialize the bot application"""
    global bot_app, event_loop
    
    try:
        logger.info("Initializing bot...")
        
        # Start event loop in separate thread
        loop_thread = Thread(target=run_async_loop, daemon=True)
        loop_thread.start()
        
        # Wait for event loop to be ready
        import time
        time.sleep(0.5)
        
        # Create bot application
        bot_app = create_application()
        
        # Initialize the application
        future = asyncio.run_coroutine_threadsafe(bot_app.initialize(), event_loop)
        future.result(timeout=30)
        
        logger.info("Bot initialized and ready to receive webhooks")
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize bot: {e}", exc_info=True)
        return False


# Initialize bot on startup
if __name__ != '__main__':
    # Running under gunicorn/production server
    if not initialize_bot():
        logger.error("Bot initialization failed!")
        raise RuntimeError("Bot initialization failed")


if __name__ == '__main__':
    # Development mode
    logger.info("Starting in development mode...")
    
    if not initialize_bot():
        logger.error("Bot initialization failed!")
        exit(1)
    
    # Run Flask app
    port = int(os.environ.get('PORT', 10000))
    logger.info(f"Starting Flask server on port {port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
