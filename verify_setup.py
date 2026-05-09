#!/usr/bin/env python3
"""
Installation Verification Script
Run this to verify your bot setup is correct
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 12:
        print("✅ Python version: {}.{}.{} (OK)".format(version.major, version.minor, version.micro))
        return True
    else:
        print("❌ Python version: {}.{}.{} (Need 3.12+)".format(version.major, version.minor, version.micro))
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'telegram',
        'requests',
        'dotenv',
        'aiohttp',
        'aiofiles'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} NOT installed")
            missing.append(package)
    
    return len(missing) == 0

def check_directories():
    """Check if required directories exist"""
    dirs = ['handlers', 'services', 'utils', 'logs', 'temp']
    all_exist = True
    
    for dir_name in dirs:
        if os.path.isdir(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory missing")
            all_exist = False
    
    return all_exist

def check_files():
    """Check if required files exist"""
    files = [
        'bot.py',
        'config.py',
        'requirements.txt',
        '.env.example',
        'handlers/__init__.py',
        'handlers/start_handler.py',
        'handlers/repo_handler.py',
        'services/__init__.py',
        'services/github_service.py',
        'services/telegram_service.py',
        'utils/__init__.py',
        'utils/validators.py',
        'utils/cleanup.py',
        'utils/logger.py'
    ]
    
    all_exist = True
    for file_name in files:
        if os.path.isfile(file_name):
            print(f"✅ {file_name} exists")
        else:
            print(f"❌ {file_name} missing")
            all_exist = False
    
    return all_exist

def check_env_file():
    """Check if .env file exists and has token"""
    if not os.path.isfile('.env'):
        print("❌ .env file not found")
        print("   → Copy .env.example to .env and add your bot token")
        return False
    
    print("✅ .env file exists")
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'your_bot_token_here' in content:
            print("⚠️  .env file still has placeholder token")
            print("   → Edit .env and add your real bot token")
            return False
        elif 'TELEGRAM_BOT_TOKEN=' in content:
            print("✅ Bot token appears to be configured")
            return True
        else:
            print("❌ TELEGRAM_BOT_TOKEN not found in .env")
            return False

def check_config():
    """Check if config loads correctly"""
    try:
        from config import config
        print("✅ Config module loads successfully")
        
        if config.TELEGRAM_BOT_TOKEN:
            print("✅ Bot token is set")
            return True
        else:
            print("❌ Bot token is not set")
            return False
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("GitHub Repository Downloader Bot - Installation Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Files", check_files),
        ("Environment File", check_env_file),
        ("Configuration", check_config)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n📋 Checking {name}...")
        print("-" * 60)
        result = check_func()
        results.append((name, result))
        print()
    
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print()
    
    if all_passed:
        print("🎉 All checks passed! Your bot is ready to run.")
        print()
        print("Next steps:")
        print("1. Run: python bot.py")
        print("2. Open Telegram and search for your bot")
        print("3. Send /start command")
        print("4. Try downloading a repository!")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print()
        print("Common fixes:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Create .env file: cp .env.example .env")
        print("3. Edit .env and add your bot token")
        print("4. Make sure all files are present")
    
    print()
    print("For help, read:")
    print("- QUICKSTART.md (5-minute setup)")
    print("- SETUP_GUIDE.md (detailed guide)")
    print("- TROUBLESHOOTING.md (problem solving)")
    print()

if __name__ == '__main__':
    main()
