import re
from typing import Optional, Tuple

class GitHubValidator:
    """Validate GitHub repository URLs"""
    
    GITHUB_URL_PATTERN = re.compile(
        r'^https?://(?:www\.)?github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9._-]+?)(?:\.git)?/?$'
    )
    
    @classmethod
    def validate_url(cls, url: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate GitHub URL and extract owner and repo name
        
        Returns:
            (is_valid, owner, repo_name)
        """
        url = url.strip()
        match = cls.GITHUB_URL_PATTERN.match(url)
        
        if not match:
            return False, None, None
        
        owner, repo = match.groups()
        return True, owner, repo
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename to prevent path traversal"""
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = filename.replace('..', '_')
        return filename[:255]
