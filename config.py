"""
Bot configuration file
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file FIRST
load_dotenv()


class Config:
    """Bot configuration class"""
    def __init__(self):
        # Bot token from @BotFather
        self.BOT_TOKEN: str = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
        
        # Channel ID (use @username or -100xxxxxxxxxx format)
        self.CHANNEL_ID: str = os.getenv("CHANNEL_ID", "@your_channel")
        
        # Channel link for users to subscribe
        self.CHANNEL_LINK: str = os.getenv("CHANNEL_LINK", "https://t.me/your_channel")
        
        # Database file path
        self.DATABASE_PATH: str = "bot_database.db"
        
        # Bot username (without @)
        self.BOT_USERNAME: str = os.getenv("BOT_USERNAME", "your_bot_username")
        
        # Admin user ID (Telegram ID of admin who can use /stats)
        self.ADMIN_USER_ID: int = int(os.getenv("ADMIN_USER_ID", "0"))
        
        # Points per referral
        self.POINTS_PER_REFERRAL: int = 1


config = Config()

