"""
Test broadcast script
Sends a test message to a specific user (you) before broadcasting to everyone
Usage: python test_broadcast.py YOUR_USER_ID "Test message"
"""
import asyncio
import logging
import sys
import argparse

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def send_test_message(user_id: int, message: str):
    """Send a test message to a specific user"""
    # Validate configuration
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Bot token not configured! Please set BOT_TOKEN in environment")
        sys.exit(1)
    
    # Initialize bot
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    try:
        logger.info(f"Sending test message to user {user_id}...")
        await bot.send_message(chat_id=user_id, text=message)
        logger.info("✓ Test message sent successfully!")
        print(f"\n✅ Message successfully sent to user {user_id}")
        print("\nIf you received the message correctly, you can proceed with the full broadcast using:")
        print(f'python broadcast.py "{message}"')
    except Exception as e:
        logger.error(f"✗ Failed to send test message: {e}")
        print(f"\n❌ Error: {e}")
        print("\nPossible issues:")
        print("1. User ID is incorrect")
        print("2. User has blocked the bot")
        print("3. Bot token is invalid")
    finally:
        await bot.session.close()


def main():
    """Main function to parse arguments and send test"""
    parser = argparse.ArgumentParser(
        description='Send a test message to verify broadcast functionality',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python test_broadcast.py 123456789 "Test message"
  python test_broadcast.py 987654321 "Hello! This is a test 🎉"
        """
    )
    
    parser.add_argument(
        'user_id',
        type=int,
        help='Telegram user ID to send test message to'
    )
    
    parser.add_argument(
        'message',
        help='Test message to send'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*50)
    print("TEST BROADCAST")
    print("="*50)
    print(f"Recipient: {args.user_id}")
    print(f"Message: {args.message}")
    print("="*50 + "\n")
    
    # Run test
    try:
        asyncio.run(send_test_message(args.user_id, args.message))
    except KeyboardInterrupt:
        logger.info("\nTest interrupted by user")
    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

