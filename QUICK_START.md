# Quick Start Guide - Broadcast Script

## 🚀 Quick Usage

### Step 1: Test First (Recommended)
Send a test message to yourself first:

```bash
python test_broadcast.py YOUR_TELEGRAM_USER_ID "This is a test message"
```

**How to find your Telegram User ID:**
1. Start a chat with `@userinfobot` on Telegram
2. It will reply with your user ID
3. Use that number in the command above

### Step 2: Broadcast to Everyone
Once the test works, broadcast to all users:

```bash
python broadcast.py "Your message here"
```

The script will ask for confirmation before sending!

## 📝 Examples

### Simple Message
```bash
python broadcast.py "Hello everyone! 👋"
```

### Formatted Message
```bash
python broadcast.py "<b>Important Update!</b>

We've added new features to the bot. Check them out!"
```

### With Emojis
```bash
python broadcast.py "🎉 Special announcement! Refer your friends and earn rewards! 🎁"
```

## ⚙️ How It Works

1. **Gets all users** from your database
2. **Sends messages** in batches of 20
3. **Rests 5 seconds** between batches (prevents rate limiting)
4. **Logs everything** to console and `broadcast.log`
5. **Shows summary** at the end

## 📊 Rate Limiting Details

- **Batch size**: 20 messages
- **Rest time**: 5 seconds between batches
- **Delay between messages**: 0.05 seconds

This means:
- 100 users = ~25 seconds total
- 500 users = ~2 minutes total
- 1000 users = ~4 minutes total

## 🛡️ Safety Features

✅ Confirmation prompt before sending  
✅ Detailed logging of all actions  
✅ Graceful error handling  
✅ Won't hit Telegram rate limits  
✅ Can interrupt with Ctrl+C  

## 📁 Files Created

- `broadcast.py` - Main broadcast script
- `test_broadcast.py` - Test script for single user
- `broadcast.log` - Log file with all broadcast history
- `BROADCAST_README.md` - Detailed documentation
- `QUICK_START.md` - This quick reference guide

## ❓ Need Help?

Check `BROADCAST_README.md` for detailed documentation including:
- HTML formatting examples
- Troubleshooting guide
- Advanced configuration
- More examples

## 🔧 Requirements

All requirements are already installed (same as your main bot):
- aiogram
- python-dotenv
- sqlite3 (built-in)

No additional setup needed! 🎉

