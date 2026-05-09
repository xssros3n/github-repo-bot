import aiohttp
import asyncio
from typing import Optional, Dict, Any
from config import config
from utils.logger import logger

class GitHubService:
    """Handle GitHub API interactions"""
    
    def __init__(self):
        self.base_url = config.GITHUB_API_BASE
        self.headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Repo-Telegram-Bot'
        }
        if config.GITHUB_TOKEN:
            self.headers['Authorization'] = f'token {config.GITHUB_TOKEN}'
    
    async def get_repo_info(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Get repository information from GitHub API"""
        url = f"{self.base_url}/repos/{owner}/{repo}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=10)) as response:
                    if response.status == 200:
                        data = await response.json()
                        logger.info(f"Retrieved info for {owner}/{repo}")
                        return data
                    elif response.status == 404:
                        logger.warning(f"Repository not found: {owner}/{repo}")
                        return None
                    else:
                        logger.error(f"GitHub API error: {response.status}")
                        return None
        except asyncio.TimeoutError:
            logger.error(f"Timeout getting repo info for {owner}/{repo}")
            return None
        except Exception as e:
            logger.error(f"Error getting repo info: {e}")
            return None
    
    async def download_repo_zip(self, owner: str, repo: str, branch: str, output_path: str) -> bool:
        """Download repository as ZIP file"""
        url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=config.DOWNLOAD_TIMEOUT)) as response:
                    if response.status == 200:
                        total_size = int(response.headers.get('content-length', 0))
                        
                        if total_size > config.MAX_FILE_SIZE_BYTES:
                            logger.warning(f"File too large: {total_size} bytes")
                            return False
                        
                        with open(output_path, 'wb') as f:
                            async for chunk in response.content.iter_chunked(8192):
                                f.write(chunk)
                        
                        logger.info(f"Downloaded {owner}/{repo} to {output_path}")
                        return True
                    else:
                        logger.error(f"Download failed with status: {response.status}")
                        return False
        except asyncio.TimeoutError:
            logger.error(f"Download timeout for {owner}/{repo}")
            return False
        except Exception as e:
            logger.error(f"Download error: {e}")
            return False
    
    def get_default_branch(self, repo_info: Dict[str, Any]) -> str:
        """Extract default branch from repo info"""
        return repo_info.get('default_branch', 'main')
    
    def get_repo_size_mb(self, repo_info: Dict[str, Any]) -> float:
        """Get repository size in MB"""
        size_kb = repo_info.get('size', 0)
        return size_kb / 1024
    
    def is_private(self, repo_info: Dict[str, Any]) -> bool:
        """Check if repository is private"""
        return repo_info.get('private', True)
