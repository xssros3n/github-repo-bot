# Render Deployment Fix

## Problem
Render was failing with "Port scan timeout reached, no open ports detected" because Flask async routes don't work properly with gunicorn's gthread worker.

## Solution Applied

### 1. Fixed Flask Routes
- Converted all async routes to synchronous
- Health check route now returns simple "Bot is running" text
- Webhook route processes updates via `asyncio.run_coroutine_threadsafe()`

### 2. Event Loop Management
- Created dedicated event loop running in separate daemon thread
- All async operations now use `asyncio.run_coroutine_threadsafe()` to interact with the loop
- Ensures proper async/sync bridge for Flask + python-telegram-bot

### 3. Port Configuration
- Flask binds to `0.0.0.0:$PORT` (Render provides PORT env variable)
- Default port: 10000 (Render's standard)
- Health check at `/` returns 200 OK

### 4. Gunicorn Configuration
```
gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 --worker-class gthread
```

## Key Changes in app.py

1. **Added event loop thread**:
```python
def run_async_loop():
    global event_loop
    event_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(event_loop)
    event_loop.run_forever()
```

2. **Synchronous webhook handler**:
```python
@app.route(f'/{config.TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot_app.bot)
    asyncio.run_coroutine_threadsafe(bot_app.process_update(update), event_loop)
    return jsonify({'ok': True}), 200
```

3. **Simple health check**:
```python
@app.route('/', methods=['GET'])
def health_check():
    return "Bot is running", 200
```

## Deployment Steps

1. **Push to GitHub**:
```bash
git add .
git commit -m "Fix Render port exposure"
git push origin main
```

2. **Render will auto-deploy** and detect the open HTTP port

3. **Verify deployment**:
- Check Render logs for "Starting Flask server on port 10000"
- Visit `https://your-app.onrender.com/` - should show "Bot is running"
- Check `/webhook_info` endpoint for webhook status

## Environment Variables Required

- `TELEGRAM_BOT_TOKEN` - Your bot token
- `WEBHOOK_URL` - Your Render app URL (e.g., https://your-app.onrender.com)
- `GITHUB_TOKEN` - (Optional) For higher rate limits
- `PORT` - Auto-provided by Render (10000)

## Testing

1. Health check: `curl https://your-app.onrender.com/`
2. Webhook info: `curl https://your-app.onrender.com/webhook_info`
3. Send message to bot on Telegram

## What This Fixes

✅ HTTP port properly exposed on 0.0.0.0:$PORT
✅ Render health checks pass
✅ Flask routes work with gunicorn
✅ Async telegram bot operations work correctly
✅ Webhook receives and processes updates
✅ No more "port scan timeout" errors
