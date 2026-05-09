@echo off
REM Prepare bot for TeleBotHost deployment

echo ========================================================
echo Preparing GitHub Repo Downloader Bot for TeleBotHost
echo ========================================================
echo.

REM Check if git is initialized
if not exist ".git\" (
    echo Initializing git repository...
    git init
    echo Git initialized
) else (
    echo Git already initialized
)

REM Add all files
echo.
echo Adding files to git...
git add .

REM Commit
echo Creating commit...
git commit -m "Prepare for TeleBotHost deployment"

echo.
echo ========================================================
echo Bot is ready for TeleBotHost deployment!
echo ========================================================
echo.
echo Next steps:
echo 1. Create repository on GitHub/GitLab
echo 2. Add remote: git remote add origin your-repo-url
echo 3. Push code: git push -u origin main
echo 4. Go to https://console.telebothost.com/
echo 5. Create new bot and connect your repository
echo 6. Add environment variables:
echo    - TELEGRAM_BOT_TOKEN
echo    - GITHUB_TOKEN (optional)
echo 7. Deploy!
echo.
echo Read TELEBOTHOST_DEPLOYMENT.md for detailed instructions
echo.
pause
