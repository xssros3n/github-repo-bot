#!/bin/bash
# GitHub Repository Downloader Bot - Automated Setup Script for Linux/macOS
# This script automates the entire setup process

set -e  # Exit on error

echo "========================================"
echo "GitHub Repository Downloader Bot"
echo "Automated Setup Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
echo "[1/6] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.12+ first:"
    echo "  Ubuntu/Debian: sudo apt install python3.12 python3-pip python3-venv"
    echo "  macOS: brew install python@3.12"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}Python found: $PYTHON_VERSION${NC}"
echo ""

# Check Python version
echo "[2/6] Verifying Python version..."
python3 -c "import sys; exit(0 if sys.version_info >= (3, 12) else 1)" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Python 3.12 or higher is required${NC}"
    echo "Current version: $PYTHON_VERSION"
    echo "Please upgrade your Python installation"
    exit 1
fi
echo -e "${GREEN}Python version is compatible!${NC}"
echo ""

# Create virtual environment
echo "[3/6] Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}Virtual environment already exists, skipping...${NC}"
else
    python3 -m venv venv
    echo -e "${GREEN}Virtual environment created!${NC}"
fi
echo ""

# Activate virtual environment
echo "[4/6] Activating virtual environment..."
source venv/bin/activate
echo -e "${GREEN}Virtual environment activated!${NC}"
echo ""

# Install dependencies
echo "[5/6] Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo -e "${RED}ERROR: Failed to install dependencies${NC}"
    echo "Trying again with verbose output..."
    pip install -r requirements.txt
    exit 1
fi
echo -e "${GREEN}Dependencies installed successfully!${NC}"
echo ""

# Setup .env file
echo "[6/6] Setting up configuration..."
if [ -f ".env" ]; then
    echo -e "${YELLOW}.env file already exists${NC}"
    echo "Skipping configuration setup"
else
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}.env file created from template${NC}"
        echo ""
        echo "========================================"
        echo -e "${YELLOW}IMPORTANT: Configure your bot token!${NC}"
        echo "========================================"
        echo ""
        echo "Please edit the .env file and add your Telegram bot token"
        echo ""
        echo "Steps:"
        echo "1. Open Telegram and search for @BotFather"
        echo "2. Send /newbot and follow instructions"
        echo "3. Copy the token you receive"
        echo "4. Edit .env file: nano .env"
        echo "5. Replace 'your_bot_token_here' with your actual token"
        echo "6. Save the file (Ctrl+X, Y, Enter)"
        echo ""
        read -p "Press Enter to open .env file in editor..."
        
        # Try to open with available editor
        if command -v nano &> /dev/null; then
            nano .env
        elif command -v vim &> /dev/null; then
            vim .env
        elif command -v vi &> /dev/null; then
            vi .env
        else
            echo -e "${YELLOW}No text editor found. Please edit .env manually${NC}"
        fi
    else
        echo -e "${RED}ERROR: .env.example file not found${NC}"
        exit 1
    fi
fi
echo ""

# Run verification
echo "========================================"
echo "Running installation verification..."
echo "========================================"
echo ""
python verify_setup.py
echo ""

# Final instructions
echo "========================================"
echo -e "${GREEN}Setup Complete!${NC}"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Make sure you've added your bot token to .env file"
echo "2. Run the bot with: python bot.py"
echo "3. Or simply run: ./run.sh"
echo ""
read -p "Do you want to start the bot now? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "========================================"
    echo "Starting bot..."
    echo "========================================"
    echo "Press Ctrl+C to stop the bot"
    echo ""
    python bot.py
fi
