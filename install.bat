@echo off
REM GitHub Repository Downloader Bot - Automated Setup Script for Windows
REM This script automates the entire setup process

echo ========================================
echo GitHub Repository Downloader Bot
echo Automated Setup Script
echo ========================================
echo.

REM Check if Python is installed
echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.12+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

python --version
echo Python found!
echo.

REM Check Python version
echo [2/6] Verifying Python version...
python -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)"
if errorlevel 1 (
    echo ERROR: Python 3.12 or higher is required
    echo Please upgrade your Python installation
    pause
    exit /b 1
)
echo Python version is compatible!
echo.

REM Create virtual environment
echo [3/6] Creating virtual environment...
if exist "venv\" (
    echo Virtual environment already exists, skipping...
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
)
echo.

REM Activate virtual environment
echo [4/6] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

REM Install dependencies
echo [5/6] Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Trying again with verbose output...
    pip install -r requirements.txt
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

REM Setup .env file
echo [6/6] Setting up configuration...
if exist ".env" (
    echo .env file already exists
    echo Skipping configuration setup
) else (
    if exist ".env.example" (
        copy .env.example .env >nul
        echo .env file created from template
        echo.
        echo ========================================
        echo IMPORTANT: Configure your bot token!
        echo ========================================
        echo.
        echo Please edit the .env file and add your Telegram bot token
        echo.
        echo Steps:
        echo 1. Open Telegram and search for @BotFather
        echo 2. Send /newbot and follow instructions
        echo 3. Copy the token you receive
        echo 4. Open .env file in this directory
        echo 5. Replace 'your_bot_token_here' with your actual token
        echo 6. Save the file
        echo.
        echo Press any key to open .env file in Notepad...
        pause >nul
        notepad .env
    ) else (
        echo ERROR: .env.example file not found
        pause
        exit /b 1
    )
)
echo.

REM Run verification
echo ========================================
echo Running installation verification...
echo ========================================
echo.
python verify_setup.py
echo.

REM Final instructions
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure you've added your bot token to .env file
echo 2. Run the bot with: python bot.py
echo 3. Or simply run: run.bat
echo.
echo To start the bot now, press any key...
echo To exit, close this window
pause >nul

REM Start the bot
echo.
echo ========================================
echo Starting bot...
echo ========================================
echo Press Ctrl+C to stop the bot
echo.
python bot.py

pause
