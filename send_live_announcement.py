"""
Send YouTube Live announcement with banner2.jpg
Ready to run script - no arguments needed
"""
import asyncio
import logging
import sys
import sqlite3
from typing import List
import os

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
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

# Broadcast content
PHOTO_PATH = "assets/banner2.jpg"
CAPTION = "Biz boshladik: https://youtube.com/live/lrK6rcXA0Lc?feature=share"


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


async def send_photo_to_user(bot: Bot, user_id: int, photo: FSInputFile, caption: str) -> bool:
    """Send photo with caption to a single user"""
    try:
        await bot.send_photo(chat_id=user_id, photo=photo, caption=caption)
        logger.info(f"✓ Photo sent to user {user_id}")
        return True
    except Exception as e:
        logger.warning(f"✗ Failed to send photo to user {user_id}: {e}")
        return False


async def broadcast_live_announcement():
    """Broadcast YouTube Live announcement to all users"""
    # Validate photo file
    if not os.path.exists(PHOTO_PATH):
        logger.error(f"Photo file not found: {PHOTO_PATH}")
        print(f"\n❌ Error: Photo file not found at {PHOTO_PATH}")
        print("Please make sure banner2.jpg exists in the assets folder.")
        sys.exit(1)
    
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
    
    logger.info(f"Starting YouTube Live announcement broadcast to {total_users} users...")
    logger.info(f"Photo: {PHOTO_PATH}")
    logger.info(f"Caption: {CAPTION}")
    logger.info(f"Rate limiting: {MESSAGES_PER_BATCH} messages per batch, {REST_TIME}s rest between batches")
    
    try:
        # Process users in batches
        for i in range(0, total_users, MESSAGES_PER_BATCH):
            batch = user_ids[i:i + MESSAGES_PER_BATCH]
            batch_number = (i // MESSAGES_PER_BATCH) + 1
            total_batches = (total_users + MESSAGES_PER_BATCH - 1) // MESSAGES_PER_BATCH
            
            logger.info(f"\n--- Batch {batch_number}/{total_batches} ({len(batch)} users) ---")
            
            # Send photos to users in current batch
            for user_id in batch:
                # Create a new FSInputFile for each user
                photo = FSInputFile(PHOTO_PATH)
                result = await send_photo_to_user(bot, user_id, photo, CAPTION)
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
    """Main function"""
    print("\n" + "="*60)
    print("🎬 YOUTUBE LIVE ANNOUNCEMENT BROADCAST")
    print("="*60)
    print(f"📸 Photo: {PHOTO_PATH}")
    print(f"💬 Caption: {CAPTION}")
    print("="*60)
    
    confirmation = input("\nAre you sure you want to send this to all users? (yes/no): ")
    
    if confirmation.lower() not in ['yes', 'y']:
        print("❌ Broadcast cancelled")
        sys.exit(0)
    
    print("\n🚀 Starting broadcast...\n")
    
    # Run broadcast
    try:
        asyncio.run(broadcast_live_announcement())
    except KeyboardInterrupt:
        logger.info("\n⚠️ Broadcast interrupted by user")
        print("\n⚠️ Broadcast interrupted!")
    except Exception as e:
        logger.error(f"Broadcast failed with error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

