# Telegram Referral Bot

A feature-rich Telegram bot built with aiogram that includes channel subscription verification, referral system, and points tracking.

## Features

- ✅ Channel subscription verification
- 🔗 Unique referral links for each user
- 📊 Points system (1 point per referral)
- 📱 Contact collection
- 👥 Referral tracking
- 📚 Knowledge base
- 💾 SQLite database for data persistence

## Requirements

- Python 3.9 or higher
- aiogram 3.13.1
- SQLite3 (included with Python)

## Installation

1. Clone this repository:
```bash
git clone <your-repo-url>
cd referall
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Copy `.env.example` to `.env`
   - Edit `.env` and fill in your bot credentials:
     - `BOT_TOKEN`: Get from [@BotFather](https://t.me/BotFather)
     - `CHANNEL_ID`: Your channel username (e.g., `@mychannel`) or ID (e.g., `-1001234567890`)
     - `CHANNEL_LINK`: Your channel link (e.g., `https://t.me/mychannel`)
     - `BOT_USERNAME`: Your bot username without @ (e.g., `mybot`)

4. Alternatively, set environment variables:
```bash
export BOT_TOKEN="your_bot_token"
export CHANNEL_ID="@your_channel"
export CHANNEL_LINK="https://t.me/your_channel"
export BOT_USERNAME="your_bot_username"
```

## Getting Your Channel ID

### For Public Channels:
Use the channel username with `@` prefix: `@mychannel`

### For Private Channels:
1. Forward any message from your channel to [@userinfobot](https://t.me/userinfobot)
2. The bot will reply with the channel ID (e.g., `-1001234567890`)
3. Use this ID in your configuration

## Bot Setup

1. Create a bot with [@BotFather](https://t.me/BotFather):
   - Send `/newbot`
   - Choose a name and username
   - Save the bot token

2. Make sure your bot is an administrator in your channel with at least these permissions:
   - Read messages
   - See members

## Running the Bot

```bash
python main.py
```

The bot will start and begin polling for updates.

## Project Structure

```
referall/
├── main.py                 # Bot entry point
├── config.py              # Configuration management
├── database.py            # Database operations
├── keyboards.py           # Keyboard layouts
├── utils.py              # Utility functions
├── handlers/             # Message and callback handlers
│   ├── __init__.py
│   ├── start.py         # /start command handler
│   ├── subscription.py   # Subscription check handler
│   ├── contact.py       # Contact sharing handler
│   └── menu.py          # Main menu handlers
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── README.md            # This file
└── bot_database.db      # SQLite database (created automatically)
```

## Usage Flow

1. **User starts the bot**: `/start` or with referral link
2. **Subscription check**: Bot verifies if user is subscribed to the channel
3. **Contact collection**: User shares their phone number
4. **Referral link generation**: User receives their unique referral link
5. **Main menu**: User can access:
   - 👥 My Referrals - View all referred users
   - ⭐ My Points - Check current points
   - 📚 Knowledge Base - Learn about the system

## Referral System

- Each user gets a unique referral link: `https://t.me/your_bot?start=USER_ID`
- When a new user joins through a referral link and subscribes to the channel, the referrer gets 1 point
- Users can track their referrals and points in real-time

## Database Schema

### Users Table
- `user_id`: Telegram user ID (primary key)
- `username`: Telegram username
- `first_name`: User's first name
- `last_name`: User's last name
- `phone_number`: User's phone number
- `referrer_id`: ID of the user who referred them
- `points`: Total points earned
- `is_subscribed`: Subscription status
- `created_at`: Registration timestamp

### Referrals Table
- `id`: Auto-increment ID
- `referrer_id`: User who made the referral
- `referred_id`: User who was referred
- `created_at`: Referral timestamp

## Customization

### Changing Points Per Referral
Edit `config.py`:
```python
POINTS_PER_REFERRAL: int = 1  # Change to desired value
```

### Customizing Messages
Edit the text in the handler files under `handlers/` directory.

### Adding New Features
1. Create a new handler in `handlers/` directory
2. Register the router in `main.py`
3. Add corresponding keyboard buttons in `keyboards.py`

## Logging

The bot logs to both:
- Console (stdout)
- `bot.log` file

Log level can be adjusted in `main.py`:
```python
logging.basicConfig(level=logging.INFO)  # Change to DEBUG for more details
```

## Troubleshooting

### Bot doesn't respond
- Check if BOT_TOKEN is correct
- Verify bot is running without errors
- Check internet connection

### Subscription check fails
- Ensure bot is admin in the channel
- Verify CHANNEL_ID is correct
- Check channel permissions

### Database errors
- Ensure write permissions in bot directory
- Check if `bot_database.db` is not corrupted
- Delete database file to recreate (will lose data)

## Security Notes

- Never commit `.env` file or expose your bot token
- Keep your bot token secure
- Regularly backup your database
- Use environment variables for sensitive data

## Support

For issues and questions:
1. Check the logs in `bot.log`
2. Verify configuration in `config.py` or `.env`
3. Review the aiogram documentation: https://docs.aiogram.dev/

## License

This project is open source and available for personal and commercial use.

## Credits

Built with:
- [aiogram](https://github.com/aiogram/aiogram) - Telegram Bot framework
- [SQLite](https://www.sqlite.org/) - Database

---

Made with ❤️ for the Telegram community

# referalls
