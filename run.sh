#!/bin/bash

echo "Starting GitHub Repository Downloader Bot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo "Please copy .env.example to .env and configure your bot token."
    exit 1
fi

# Install/update dependencies
echo "Installing dependencies..."
pip install -r requirements.txt --quiet
echo ""

# Run the bot
echo "Bot is starting..."
echo "Press Ctrl+C to stop the bot"
echo ""
python bot.py
