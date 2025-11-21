# Broadcast Script Documentation

## Overview
The `broadcast.py` script allows you to send messages to all bot users from the command line. It includes built-in rate limiting to prevent hitting Telegram's rate limits.

## Features
- ✅ Sends messages to all users in the database
- ✅ Rate limiting: 20 messages per batch, 5-second rest between batches
- ✅ Detailed logging to both console and `broadcast.log` file
- ✅ Success/failure tracking for each message
- ✅ Confirmation prompt before sending
- ✅ Progress tracking with batch information
- ✅ Final summary report

## Installation
No additional installation needed. The script uses the same dependencies as your main bot.

## Usage

### Basic Usage
```bash
python broadcast.py "Your message here"
```

### With Multi-line Messages
```bash
python broadcast.py "Line 1
Line 2
Line 3"
```

Or using the `-m` flag:
```bash
python broadcast.py -m "Your message here"
```

### HTML Formatting
The script supports HTML formatting (since the bot is configured with `ParseMode.HTML`):

```bash
python broadcast.py "<b>Bold text</b> and <i>italic text</i>"
```

```bash
python broadcast.py "🎉 <b>Special Announcement!</b>

We're excited to share some <i>amazing</i> news with you!

<a href='https://example.com'>Click here</a> for more details."
```

## Rate Limiting
The script implements rate limiting to comply with Telegram's API limits:
- **Batch size**: 20 messages per batch
- **Rest time**: 5 seconds between batches
- **Individual delay**: 0.05 seconds between each message

This ensures you won't hit Telegram's rate limits, which are approximately 30 messages per second.

## Output Example
```
==================================================
BROADCAST CONFIRMATION
==================================================
Message to send:
Hello everyone! 🎉
==================================================

Are you sure you want to send this message to all users? (yes/no): yes

Starting broadcast...

2025-11-21 10:30:00 - __main__ - INFO - Found 150 users in database
2025-11-21 10:30:00 - __main__ - INFO - Starting broadcast to 150 users...
2025-11-21 10:30:00 - __main__ - INFO - Rate limiting: 20 messages per batch, 5s rest between batches

--- Batch 1/8 (20 users) ---
2025-11-21 10:30:00 - __main__ - INFO - ✓ Message sent to user 123456789
2025-11-21 10:30:01 - __main__ - INFO - ✓ Message sent to user 987654321
...
2025-11-21 10:30:05 - __main__ - INFO - Resting for 5 seconds before next batch...

--- Batch 2/8 (20 users) ---
...

==================================================
BROADCAST SUMMARY
==================================================
Total users: 150
Successful: 148
Failed: 2
Success rate: 98.67%
==================================================
```

## Logs
All broadcast activity is logged to:
- **Console**: Real-time output
- **broadcast.log**: Persistent log file for later review

## Error Handling
The script handles common errors gracefully:
- User blocked the bot → Logged as failed, continues with next user
- User account deleted → Logged as failed, continues with next user
- Network issues → Logged as failed, continues with next user
- Bot token not configured → Script exits with error

## Safety Features
1. **Confirmation prompt**: Requires explicit confirmation before sending
2. **Detailed logging**: Every action is logged for audit purposes
3. **Graceful failure**: Failed messages don't stop the entire broadcast
4. **Rate limiting**: Prevents hitting Telegram API limits

## Tips
1. **Test first**: Test with a small group before broadcasting to everyone
2. **Check logs**: Review `broadcast.log` after completion
3. **Timing**: Run broadcasts during times when your users are most active
4. **Message quality**: Proofread your message before confirming
5. **Interruption**: Press `Ctrl+C` to stop the broadcast at any time

## Troubleshooting

### "Bot token not configured"
Make sure your `.env` file contains a valid `BOT_TOKEN`.

### "No users found in database"
Verify that your `bot_database.db` file exists and contains users.

### High failure rate
- Check if your bot token is still valid
- Verify bot is not banned or restricted
- Some users may have blocked the bot (this is normal)

## Advanced Configuration
You can modify rate limiting settings in the script:
```python
MESSAGES_PER_BATCH = 20  # Change batch size
REST_TIME = 5  # Change rest time in seconds
```

## Examples

### Simple announcement
```bash
python broadcast.py "New features have been added to the bot! Check them out in the menu."
```

### Promotional message
```bash
python broadcast.py "🎁 Special offer! Refer 5 friends and get exclusive rewards!"
```

### Emergency notification
```bash
python broadcast.py "⚠️ The bot will be under maintenance for 1 hour starting at 10:00 PM."
```

### Rich formatted message
```bash
python broadcast.py "<b>📢 Important Update</b>

Dear users,

We've just released version 2.0 with these features:
• Feature 1
• Feature 2
• Feature 3

<i>Thank you for your support!</i>"
```

