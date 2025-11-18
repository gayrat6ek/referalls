"""
Utility functions
"""
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from config import config
import logging

logger = logging.getLogger(__name__)


async def check_user_subscription(bot: Bot, user_id: int) -> bool:
    """
    Check if user is subscribed to the channel
    
    Args:
        bot: Bot instance
        user_id: User's Telegram ID
        
    Returns:
        True if user is subscribed, False otherwise
    """
    try:
        member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=user_id)
        logger.info(f"User {user_id} subscription status: {member.status}")
        
        # Check if user is a member, administrator, or creator
        # Note: "left" means not subscribed, "kicked" means banned
        is_subscribed = member.status in ["member", "administrator", "creator"]
        
        if not is_subscribed:
            logger.info(f"User {user_id} is not subscribed (status: {member.status})")
        
        return is_subscribed
    except TelegramBadRequest as e:
        logger.error(f"TelegramBadRequest checking subscription for user {user_id}: {e}")
        logger.error(f"Channel ID used: {config.CHANNEL_ID}")
        logger.error("Make sure the bot is added as admin to the channel!")
        return False
    except Exception as e:
        logger.error(f"Unexpected error checking subscription for user {user_id}: {e}")
        return False


def generate_referral_link(user_id: int) -> str:
    """
    Generate referral link for user
    
    Args:
        user_id: User's Telegram ID
        
    Returns:
        Referral link
    """
    return f"https://t.me/{config.BOT_USERNAME}?start={user_id}"


def extract_referrer_id(start_param: str) -> int | None:
    """
    Extract referrer ID from start parameter
    
    Args:
        start_param: Start parameter from deep link
        
    Returns:
        Referrer ID or None if invalid
    """
    try:
        return int(start_param)
    except (ValueError, TypeError):
        return None

