import os
import time
from pathlib import Path
from typing import List
from utils.logger import logger
from config import config

class CleanupManager:
    """Manage temporary file cleanup"""
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """Delete a single file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                logger.info(f"Deleted file: {filepath}")
                return True
        except Exception as e:
            logger.error(f"Failed to delete {filepath}: {e}")
        return False
    
    @staticmethod
    def cleanup_old_files(max_age_hours: int = 1) -> int:
        """Clean up old temporary files"""
        deleted_count = 0
        temp_dir = Path(config.TEMP_DIR)
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        try:
            for file_path in temp_dir.glob('*.zip'):
                if current_time - file_path.stat().st_mtime > max_age_seconds:
                    if CleanupManager.delete_file(str(file_path)):
                        deleted_count += 1
        except Exception as e:
            logger.error(f"Cleanup error: {e}")
        
        if deleted_count > 0:
            logger.info(f"Cleaned up {deleted_count} old files")
        
        return deleted_count
    
    @staticmethod
    def get_temp_files() -> List[str]:
        """Get list of temporary files"""
        temp_dir = Path(config.TEMP_DIR)
        return [str(f) for f in temp_dir.glob('*.zip')]
