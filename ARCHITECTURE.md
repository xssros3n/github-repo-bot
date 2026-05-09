# 🏗️ Architecture & Code Explanation

## Project Architecture

This bot follows a clean, modular architecture with separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                        bot.py                           │
│                   (Entry Point)                         │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │Handlers │  │Services │  │  Utils  │
   └─────────┘  └─────────┘  └─────────┘
        │            │            │
        │            │            │
   ┌────┴────┐  ┌────┴────┐  ┌────┴────┐
   │ Start   │  │ GitHub  │  │Validator│
   │ Repo    │  │Telegram │  │ Logger  │
   └─────────┘  └─────────┘  │ Cleanup │
                              └─────────┘
```

## Core Components

### 1. bot.py (Main Entry Point)

**Purpose:** Initialize and run the bot

**Key Functions:**
- `main()`: Entry point, validates config and starts bot
- `error_handler()`: Global error handling
- `post_init()`: Initialize bot data after startup
- `post_shutdown()`: Cleanup before shutdown

**Flow:**
```python
1. Load configuration from .env
2. Validate required settings
3. Create Telegram Application
4. Register command handlers
5. Register message handlers
6. Start polling for updates
```

### 2. config.py (Configuration Management)

**Purpose:** Centralized configuration from environment variables

**Key Features:**
- Loads `.env` file automatically
- Provides default values
- Validates required settings
- Creates necessary directories

**Important Settings:**
```python
TELEGRAM_BOT_TOKEN      # Required: Your bot token
RATE_LIMIT_REQUESTS     # Max requests per time window
MAX_FILE_SIZE_MB        # Maximum download size
DOWNLOAD_TIMEOUT        # Download timeout in seconds
GITHUB_TOKEN            # Optional: Increases API limits
```

### 3. Handlers Layer

#### handlers/start_handler.py

**Commands:**
- `/start` - Welcome message with instructions
- `/help` - Detailed help and limitations
- `/stats` - User statistics

**Code Flow:**
```python
User sends /start
    ↓
Extract user info
    ↓
Log the interaction
    ↓
Send formatted welcome message
```

#### handlers/repo_handler.py

**Purpose:** Process GitHub repository URLs

**Flow:**
```python
1. Receive message from user
2. Check rate limit
3. Validate GitHub URL
4. Extract owner and repo name
5. Fetch repository info from GitHub API
6. Validate repository (public, size)
7. Download ZIP file
8. Send to user via Telegram
9. Cleanup temporary file
10. Update user statistics
```

**Rate Limiting:**
```python
user_requests = {
    user_id: [timestamp1, timestamp2, ...]
}

# Remove old timestamps outside window
# Check if count < limit
# Add new timestamp
```

### 4. Services Layer

#### services/github_service.py

**Purpose:** Interact with GitHub API

**Key Methods:**

1. `get_repo_info(owner, repo)` - Fetch repository metadata
   ```python
   GET https://api.github.com/repos/{owner}/{repo}
   Returns: {
       "default_branch": "main",
       "size": 1234,
       "private": false,
       "stargazers_count": 100,
       ...
   }
   ```

2. `download_repo_zip(owner, repo, branch, output_path)` - Download ZIP
   ```python
   GET https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip
   Stream to file in chunks
   Validate size during download
   ```

3. `get_default_branch(repo_info)` - Extract default branch
4. `is_private(repo_info)` - Check if repository is private

**Authentication:**
- Uses GitHub token if provided (increases rate limit)
- Falls back to unauthenticated requests

#### services/telegram_service.py

**Purpose:** Telegram bot utilities

**Key Methods:**

1. `send_message()` - Send text message
2. `edit_message()` - Edit existing message (for progress updates)
3. `send_document()` - Send ZIP file
4. `format_repo_info()` - Format repository data for display

**Message Formatting:**
```python
Uses HTML parse mode:
<b>Bold</b>
<code>Code</code>
<i>Italic</i>
```

### 5. Utils Layer

#### utils/validators.py

**Purpose:** Input validation and sanitization

**GitHubValidator Class:**

1. `validate_url(url)` - Validate and parse GitHub URL
   ```python
   Pattern: https://github.com/{owner}/{repo}
   Returns: (is_valid, owner, repo)
   ```

2. `sanitize_filename(filename)` - Prevent path traversal
   ```python
   Remove: < > : " / \ | ? *
   Replace: .. with _
   Limit: 255 characters
   ```

**Security:**
- Regex validation prevents injection
- Filename sanitization prevents path traversal
- Only allows github.com domain

#### utils/cleanup.py

**Purpose:** Manage temporary files

**CleanupManager Class:**

1. `delete_file(filepath)` - Delete single file safely
2. `cleanup_old_files(max_age_hours)` - Remove old temp files
3. `get_temp_files()` - List all temporary files

**Automatic Cleanup:**
- After each successful send
- On bot shutdown
- Scheduled cleanup of old files

#### utils/logger.py

**Purpose:** Centralized logging

**Features:**
- Console output (INFO level)
- File output (DEBUG level)
- Daily log rotation
- Formatted timestamps
- Function name and line numbers in file logs

**Log Levels:**
```python
DEBUG   - Detailed information
INFO    - General information
WARNING - Warning messages
ERROR   - Error messages
```

## Data Flow

### Download Repository Flow

```
User sends URL
    ↓
[Rate Limit Check]
    ↓
[URL Validation] → Invalid → Send error
    ↓ Valid
[GitHub API Call]
    ↓
[Repository Info] → Not found/Private → Send error
    ↓ Valid
[Size Check] → Too large → Send error
    ↓ OK
[Show Repo Info]
    ↓
[Download ZIP]
    ↓
[Upload to Telegram]
    ↓
[Cleanup File]
    ↓
[Update Stats]
```

## Security Features

### 1. Input Validation
```python
# URL validation with regex
GITHUB_URL_PATTERN = re.compile(
    r'^https?://(?:www\.)?github\.com/([a-zA-Z0-9_-]+)/([a-zA-Z0-9._-]+?)(?:\.git)?/?$'
)
```

### 2. Filename Sanitization
```python
# Remove dangerous characters
filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
# Prevent path traversal
filename = filename.replace('..', '_')
```

### 3. Rate Limiting
```python
# Per-user request tracking
# Time-window based limiting
# Automatic cleanup of old requests
```

### 4. File Size Validation
```python
# Check before download
# Check during download
# Configurable limits
```

### 5. Private Repository Protection
```python
# API check for private flag
# Only allow public repositories
```

## Async Architecture

### Why Async?

1. **Non-blocking I/O** - Multiple downloads simultaneously
2. **Better performance** - Don't wait for network operations
3. **Scalability** - Handle many users concurrently

### Async Functions

```python
async def get_repo_info()      # GitHub API call
async def download_repo_zip()  # File download
async def handle_repo_url()    # Main handler
```

### Async Context Managers

```python
async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
        # Non-blocking download
```

## Error Handling

### Levels of Error Handling

1. **Function Level**
   ```python
   try:
       # Operation
   except SpecificError as e:
       logger.error(f"Error: {e}")
       return None
   ```

2. **Handler Level**
   ```python
   # Validate input
   # Check conditions
   # Send user-friendly error messages
   ```

3. **Global Level**
   ```python
   async def error_handler(update, context):
       # Catch all unhandled errors
       # Log and notify user
   ```

## Performance Optimizations

### 1. Streaming Downloads
```python
# Don't load entire file in memory
async for chunk in response.content.iter_chunked(8192):
    f.write(chunk)
```

### 2. Automatic Cleanup
```python
# Delete files immediately after sending
# Periodic cleanup of old files
```

### 3. Efficient Rate Limiting
```python
# In-memory tracking
# Automatic expiration
# No database needed
```

### 4. Connection Pooling
```python
# aiohttp manages connection pool
# Reuses connections
```

## Extensibility

### Adding New Commands

1. Create handler function:
```python
async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Response")
```

2. Register in bot.py:
```python
application.add_handler(CommandHandler("newcmd", new_command))
```

### Adding New Features

1. **Database Integration**
   - Add SQLAlchemy or similar
   - Create models in new `models/` directory
   - Update handlers to use database

2. **Admin Panel**
   - Create `handlers/admin_handler.py`
   - Add admin check decorator
   - Implement admin commands

3. **Multiple File Formats**
   - Extend `github_service.py`
   - Add format selection in handler
   - Update download logic

## Testing

### Manual Testing Checklist

- [ ] /start command works
- [ ] /help command works
- [ ] /stats command works
- [ ] Valid GitHub URL downloads
- [ ] Invalid URL shows error
- [ ] Private repo shows error
- [ ] Large repo shows error
- [ ] Rate limit works
- [ ] File cleanup works
- [ ] Logs are created

### Test URLs

```
Valid:
https://github.com/octocat/Hello-World

Invalid:
https://gitlab.com/user/repo
https://github.com/nonexistent/repo
https://github.com/private/repo
```

## Monitoring

### Key Metrics to Monitor

1. **Bot Health**
   - Uptime
   - Error rate
   - Response time

2. **Usage Statistics**
   - Total downloads
   - Active users
   - Popular repositories

3. **System Resources**
   - Disk space (temp directory)
   - Memory usage
   - CPU usage

4. **API Limits**
   - GitHub API rate limit
   - Telegram API rate limit

### Log Analysis

```bash
# Count errors
grep ERROR logs/bot_*.log | wc -l

# Most downloaded repos
grep "Successfully sent" logs/bot_*.log | cut -d' ' -f10 | sort | uniq -c | sort -rn

# Active users
grep "User" logs/bot_*.log | cut -d' ' -f6 | sort -u | wc -l
```

## Best Practices Used

1. ✅ **Separation of Concerns** - Handlers, Services, Utils
2. ✅ **Type Hints** - Better code documentation
3. ✅ **Async/Await** - Non-blocking operations
4. ✅ **Error Handling** - Try/except everywhere
5. ✅ **Logging** - Comprehensive logging
6. ✅ **Configuration** - Environment variables
7. ✅ **Security** - Input validation, sanitization
8. ✅ **Documentation** - Comments and docstrings
9. ✅ **Modularity** - Easy to extend
10. ✅ **Clean Code** - Readable and maintainable

---

This architecture ensures the bot is:
- **Reliable** - Proper error handling
- **Secure** - Input validation and sanitization
- **Scalable** - Async architecture
- **Maintainable** - Clean code structure
- **Extensible** - Easy to add features
