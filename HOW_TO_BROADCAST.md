# How to Broadcast Messages

## 🎬 Send YouTube Live Announcement (Ready to Use!)

### Quick Command - Just Run This:
```bash
python send_live_announcement.py
```

This will send:
- **Photo**: `assets/banner2.jpg`
- **Caption**: "Biz boshladik: https://youtube.com/live/lrK6rcXA0Lc?feature=share"

The script will:
1. Show you what will be sent
2. Ask for confirmation
3. Send to all users with rate limiting (20 per batch, 5 second rest)
4. Show progress and final summary

---

## 📝 Other Broadcast Options

### 1. Send Text Message Only
```bash
python broadcast.py "Your message here"
```

**Example:**
```bash
python broadcast.py "Yangi xususiyatlar qo'shildi! Botni sinab ko'ring."
```

### 2. Send Any Photo with Caption
```bash
python broadcast_photo.py <photo_path> "Your caption"
```

**Examples:**
```bash
python broadcast_photo.py assets/banner.jpg "Yangilik! 🎉"
python broadcast_photo.py assets/banner2.jpg "Check this out!"
```

### 3. Test Before Broadcasting
```bash
python test_broadcast.py YOUR_USER_ID "Test message"
```

**Example:**
```bash
python test_broadcast.py 123456789 "Bu test xabari"
```

---

## ⚙️ How Rate Limiting Works

- **20 messages** sent in each batch
- **5 seconds** rest between batches
- **0.05 seconds** delay between individual messages

**Time estimates:**
- 100 users ≈ 25 seconds
- 500 users ≈ 2 minutes
- 1000 users ≈ 4 minutes

---

## 📊 What You'll See

```
==================================================
🎬 YOUTUBE LIVE ANNOUNCEMENT BROADCAST
==================================================
📸 Photo: assets/banner2.jpg
💬 Caption: Biz boshladik: https://youtube.com/live/lrK6rcXA0Lc?feature=share
==================================================

Are you sure you want to send this to all users? (yes/no): yes

🚀 Starting broadcast...

Found 150 users in database
Starting YouTube Live announcement broadcast to 150 users...

--- Batch 1/8 (20 users) ---
✓ Photo sent to user 123456789
✓ Photo sent to user 987654321
...
Resting for 5 seconds before next batch...

==================================================
BROADCAST SUMMARY
==================================================
Total users: 150
Successful: 148
Failed: 2
Success rate: 98.67%
==================================================
```

---

## 🛡️ Safety Features

✅ Confirmation required before sending
✅ Rate limiting to avoid Telegram restrictions
✅ Detailed logging to `broadcast.log`
✅ Progress tracking
✅ Error handling (failed sends don't stop broadcast)
✅ Can interrupt with Ctrl+C

---

## 📁 Files Overview

| File | Purpose |
|------|---------|
| `send_live_announcement.py` | Ready-to-use script for YouTube Live announcement ⭐ |
| `broadcast.py` | Send text messages to all users |
| `broadcast_photo.py` | Send photos with captions (generic) |
| `test_broadcast.py` | Test messages before broadcasting |

---

## 💡 Tips

1. **Always test first** with `test_broadcast.py`
2. **Check your message** - there's a confirmation prompt
3. **Monitor the log** - check `broadcast.log` for details
4. **Best timing** - send when users are most active
5. **Stop anytime** - press Ctrl+C if needed

---

## ❓ Troubleshooting

### "Photo file not found"
Make sure `assets/banner2.jpg` exists:
```bash
ls -lh assets/
```

### "Bot token not configured"
Check your `.env` file has valid `BOT_TOKEN`

### High failure rate
- Some users may have blocked the bot (normal)
- Check bot token is still valid
- Verify bot permissions

### Script hangs
- Check internet connection
- Verify bot token is active
- Look at `broadcast.log` for errors

---

## 🚀 Quick Start for Your YouTube Live

Just run:
```bash
python send_live_announcement.py
```

Type `yes` when prompted, and it will send to all users! 🎉

