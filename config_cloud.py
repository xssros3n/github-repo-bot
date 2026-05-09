import os
from dotenv import load_dotenv

load_dotenv()

class CloudConfig:
    """Optimized configuration for TeleBotHost and cloud hosting"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # Rate Limiting (adjusted for cloud - more permissive)
    RATE_LIMIT_REQUESTS = int(os.getenv('RATE_LIMIT_REQUESTS', 10))
    RATE_LIMIT_WINDOW = int(os.getenv('RATE_LIMIT_WINDOW', 60))
    
    # File Size (optimized for cloud bandwidth)
    MAX_FILE_SIZE_MB = int(os.getenv('MAX_FILE_SIZE_MB', 50))
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    # Timeouts (adjusted for cloud - faster fails)
    DOWNLOAD_TIMEOUT = int(os.getenv('DOWNLOAD_TIMEOUT', 180))
    
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
    
    # Performance settings
    CONNECTION_POOL_SIZE = int(os.getenv('CONNECTION_POOL_SIZE', 10))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required in environment variables")
        
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        os.makedirs(cls.LOGS_DIR, exist_ok=True)
        
        if cls.CLOUD_HOSTING:
            print("Cloud hosting mode enabled")
            print(f"Max concurrent downloads: {cls.MAX_CONCURRENT_DOWNLOADS}")
            print(f"Cleanup interval: {cls.CLEANUP_INTERVAL}s")

config = CloudConfig()
