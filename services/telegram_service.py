import os
from typing import Optional
from telegram import Update, Message
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from utils.logger import logger

class TelegramService:
    """Handle Telegram bot interactions"""
    
    @staticmethod
    async def send_message(update: Update, text: str, parse_mode: Optional[str] = ParseMode.HTML) -> Optional[Message]:
        """Send a message to user"""
        try:
            return await update.message.reply_text(text, parse_mode=parse_mode)
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            return None
    
    @staticmethod
    async def edit_message(message: Message, text: str, parse_mode: Optional[str] = ParseMode.HTML) -> bool:
        """Edit an existing message"""
        try:
            await message.edit_text(text, parse_mode=parse_mode)
            return True
        except Exception as e:
            logger.error(f"Failed to edit message: {e}")
            return False
    
    @staticmethod
    async def send_document(update: Update, file_path: str, caption: Optional[str] = None) -> bool:
        """Send a document to user"""
        try:
            with open(file_path, 'rb') as f:
                await update.message.reply_document(
                    document=f,
                    caption=caption,
                    filename=os.path.basename(file_path)
                )
            logger.info(f"Sent document: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to send document: {e}")
            return False
    
    @staticmethod
    def format_repo_info(repo_data: dict) -> str:
        """Format repository information for display"""
        name = repo_data.get('full_name', 'Unknown')
        description = repo_data.get('description', 'No description')
        stars = repo_data.get('stargazers_count', 0)
        forks = repo_data.get('forks_count', 0)
        language = repo_data.get('language', 'Unknown')
        size = repo_data.get('size', 0) / 1024  # Convert to MB
        
        return (
            f"📦 <b>{name}</b>\n\n"
            f"📝 {description}\n\n"
            f"⭐ Stars: {stars:,}\n"
            f"🔱 Forks: {forks:,}\n"
            f"💻 Language: {language}\n"
            f"📊 Size: {size:.2f} MB"
        )
