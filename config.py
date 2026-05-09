import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration for Render deployment"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Webhook Configuration (Required for Render)
    WEBHOOK_URL = os.getenv('WEBHOOK_URL')  # e.g., https://your-app.onrender.com
    PORT = int(os.getenv('PORT', 10000))  # Render provides PORT env variable
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 5))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))
    
    # File Size
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Timeouts
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 300))
    
    # GitHub
    GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')
    GITHUB_API_BASE = 'https://api.github.com'
    
    # Paths
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TEMP_DIR = os.path.join(BASE_DIR, 'temp')
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')  # production or development
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        
        if not cls.WEBHOOK_URL:
            raise ValueError("WEBHOOK_URL is required for webhook mode")
        
        # Create directories
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        
        # Log configuration
        print(f"Configuration loaded:")
        print(f"  - Webhook URL: {cls.WEBHOOK_URL}")
        print(f"  - Port: {cls.PORT}")
        print(f"  - Environment: {cls.ENVIRONMENT}")
        print(f"  - Max file size: {cls.MAX_FILE_SIZE_MB}MB")
        print(f"  - Rate limit: {cls.RATE_LIMIT_REQUESTS} requests per {cls.RATE_LIMIT_WINDOW}s")

config = Config()
