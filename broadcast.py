"""
Broadcast message script
Send messages to all users with rate limiting
Usage: python broadcast.py "Your message here"
"""
import asyncio
import logging
import sys
import sqlite3
from typing import List
import argparse

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('broadcast.log')
    ]
)

logger = logging.getLogger(__name__)

# Rate limiting settings
MESSAGES_PER_BATCH = 20  # Send 20 messages
REST_TIME = 5  # Rest for 5 seconds between batches


def get_all_users() -> List[int]:
    """Get all user IDs from database"""
    try:
        conn = sqlite3.connect(config.DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT user_id FROM users")
        rows = cursor.fetchall()
        conn.close()
        
        user_ids = [row[0] for row in rows]
        logger.info(f"Found {len(user_ids)} users in database")
        return user_ids
    except Exception as e:
        logger.error(f"Error getting users from database: {e}")
        return []


async def send_message_to_user(bot: Bot, user_id: int, message: str) -> bool:
    """Send message to a single user"""
    try:
        await bot.send_message(chat_id=user_id, text=message)
        logger.info(f"✓ Message sent to user {user_id}")
        return True
    except Exception as e:
        logger.warning(f"✗ Failed to send message to user {user_id}: {e}")
        return False


async def broadcast_message(message: str):
    """Broadcast message to all users with rate limiting"""
    # Validate configuration
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Bot token not configured! Please set BOT_TOKEN in environment")
        sys.exit(1)
    
    # Initialize bot
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Get all users
    user_ids = get_all_users()
    
    if not user_ids:
        logger.warning("No users found in database")
        await bot.session.close()
        return
    
    total_users = len(user_ids)
    successful = 0
    failed = 0
    
    logger.info(f"Starting broadcast to {total_users} users...")
    logger.info(f"Rate limiting: {MESSAGES_PER_BATCH} messages per batch, {REST_TIME}s rest between batches")
    
    try:
        # Process users in batches
        for i in range(0, total_users, MESSAGES_PER_BATCH):
            batch = user_ids[i:i + MESSAGES_PER_BATCH]
            batch_number = (i // MESSAGES_PER_BATCH) + 1
            total_batches = (total_users + MESSAGES_PER_BATCH - 1) // MESSAGES_PER_BATCH
            
            logger.info(f"\n--- Batch {batch_number}/{total_batches} ({len(batch)} users) ---")
            
            # Send messages to users in current batch
            for user_id in batch:
                result = await send_message_to_user(bot, user_id, message)
                if result:
                    successful += 1
                else:
                    failed += 1
                
                # Small delay between individual messages (0.05 seconds)
                await asyncio.sleep(0.05)
            
            # Rest between batches (except for the last batch)
            if i + MESSAGES_PER_BATCH < total_users:
                logger.info(f"Resting for {REST_TIME} seconds before next batch...")
                await asyncio.sleep(REST_TIME)
        
        # Print summary
        logger.info("\n" + "="*50)
        logger.info("BROADCAST SUMMARY")
        logger.info("="*50)
        logger.info(f"Total users: {total_users}")
        logger.info(f"Successful: {successful}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Success rate: {(successful/total_users*100):.2f}%")
        logger.info("="*50)
        
    finally:
        await bot.session.close()
        logger.info("Bot session closed")


def main():
    """Main function to parse arguments and start broadcast"""
    parser = argparse.ArgumentParser(
        description='Broadcast message to all bot users',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python broadcast.py "Hello everyone!"
  python broadcast.py "🎉 Special announcement: New features coming soon!"
  python broadcast.py -m "Multi-line message
with different lines"
        """
    )
    
    parser.add_argument(
        'message',
        nargs='?',
        help='Message to broadcast to all users'
    )
    
    parser.add_argument(
        '-m', '--message-arg',
        dest='message_arg',
        help='Alternative way to specify message'
    )
    
    args = parser.parse_args()
    
    # Get message from either argument
    message = args.message or args.message_arg
    
    if not message:
        parser.print_help()
        print("\n❌ Error: Message is required")
        sys.exit(1)
    
    # Confirm broadcast
    print("\n" + "="*50)
    print("BROADCAST CONFIRMATION")
    print("="*50)
    print(f"Message to send:\n{message}")
    print("="*50)
    
    confirmation = input("\nAre you sure you want to send this message to all users? (yes/no): ")
    
    if confirmation.lower() not in ['yes', 'y']:
        print("Broadcast cancelled")
        sys.exit(0)
    
    print("\nStarting broadcast...\n")
    
    # Run broadcast
    try:
        asyncio.run(broadcast_message(message))
    except KeyboardInterrupt:
        logger.info("\nBroadcast interrupted by user")
    except Exception as e:
        logger.error(f"Broadcast failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

