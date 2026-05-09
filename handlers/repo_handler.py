import os
import time
from telegram import Update
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.logger import logger
from utils.validators import GitHubValidator
from utils.cleanup import CleanupManager
from services.github_service import GitHubService
from services.telegram_service import TelegramService
from config import config

# Rate limiting storage
user_requests = {}

def check_rate_limit(user_id: int) -> bool:
    """Check if user exceeded rate limit"""
    current_time = time.time()
    
    if user_id not in user_requests:
        user_requests[user_id] = []
    
    # Remove old requests outside the time window
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if current_time - req_time < config.RATE_LIMIT_WINDOW
    ]
    
    # Check if limit exceeded
    if len(user_requests[user_id]) >= config.RATE_LIMIT_REQUESTS:
        return False
    
    # Add current request
    user_requests[user_id].append(current_time)
    return True

async def handle_repo_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle GitHub repository URL"""
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
    filename = GitHubValidator.sanitize_filename(f"{owner}_{repo}_{default_branch}.zip")
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
    
    caption = f"📦 {owner}/{repo}\n🌿 Branch: {default_branch}"
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
