"""
Send Houses Announcement with two photos and inline keyboard
Banner3.jpg and Banner4.jpg with location button
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
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
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
PHOTO1_PATH = "assets/banner3.jpg"
PHOTO2_PATH = "assets/banner4.jpg"

CAPTION = """Boshlang'ich to'lovsiz uylar soni tugayapti! 🚨

Hurmatli mijozlar!

Bizning boshlang'ich to'lovsiz berilayotgan xonadonlarga talab shunchalik yuqori bo'ldiki, ularning soni tezlik bilan kamayib bormoqda.

Rasmga e'tibor bering – bu bizning uylarimizning rejasi. Qizil va sariq rangga bo'yalgan xonadonlar allaqachon sotib bo'lingan yoki band qilingan!

Sotuv ofisimiz manzilini olish uchun quyidagi tugmani bosing👇🏻"""

# Inline keyboard with location button
def get_inline_keyboard() -> InlineKeyboardMarkup:
    """Create inline keyboard with location button"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="📍Lokatsiyani olish",
            url="https://t.me/zangiotaresidence_tjm/126"
        )]
    ])
    return keyboard


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


async def send_announcement_to_user(bot: Bot, user_id: int) -> bool:
    """Send announcement with two photos and inline keyboard"""
    try:
        # Send first photo without caption
        photo1 = FSInputFile(PHOTO1_PATH)
        await bot.send_photo(
            chat_id=user_id,
            photo=photo1
        )
        
        # Small delay between photos
        await asyncio.sleep(0.05)
        
        # Send second photo with caption and inline keyboard button
        photo2 = FSInputFile(PHOTO2_PATH)
        await bot.send_photo(
            chat_id=user_id,
            photo=photo2,
            caption=CAPTION,
            reply_markup=get_inline_keyboard()
        )
        
        logger.info(f"✓ Announcement sent to user {user_id}")
        return True
    except Exception as e:
        logger.warning(f"✗ Failed to send announcement to user {user_id}: {e}")
        return False


async def broadcast_houses_announcement():
    """Broadcast houses announcement to all users"""
    # Validate photo files
    if not os.path.exists(PHOTO1_PATH):
        logger.error(f"Photo file not found: {PHOTO1_PATH}")
        print(f"\n❌ Error: Photo file not found at {PHOTO1_PATH}")
        sys.exit(1)
    
    if not os.path.exists(PHOTO2_PATH):
        logger.error(f"Photo file not found: {PHOTO2_PATH}")
        print(f"\n❌ Error: Photo file not found at {PHOTO2_PATH}")
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
    
    logger.info(f"Starting houses announcement broadcast to {total_users} users...")
    logger.info(f"Photo 1: {PHOTO1_PATH}")
    logger.info(f"Photo 2: {PHOTO2_PATH}")
    logger.info(f"Rate limiting: {MESSAGES_PER_BATCH} messages per batch, {REST_TIME}s rest between batches")
    
    try:
        # Process users in batches
        for i in range(0, total_users, MESSAGES_PER_BATCH):
            batch = user_ids[i:i + MESSAGES_PER_BATCH]
            batch_number = (i // MESSAGES_PER_BATCH) + 1
            total_batches = (total_users + MESSAGES_PER_BATCH - 1) // MESSAGES_PER_BATCH
            
            logger.info(f"\n--- Batch {batch_number}/{total_batches} ({len(batch)} users) ---")
            
            # Send announcement to users in current batch
            for user_id in batch:
                result = await send_announcement_to_user(bot, user_id)
                if result:
                    successful += 1
                else:
                    failed += 1
                
                # Small delay between individual users (0.1 seconds)
                await asyncio.sleep(0.1)
            
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
    print("🏠 HOUSES ANNOUNCEMENT BROADCAST")
    print("="*60)
    print(f"📸 Photo 1: {PHOTO1_PATH}")
    print(f"📸 Photo 2: {PHOTO2_PATH}")
    print(f"💬 Caption: {CAPTION[:50]}...")
    print(f"🔗 Button: 📍Lokatsiyani olish")
    print("="*60)
    
    confirmation = input("\nAre you sure you want to send this to all users? (yes/no): ")
    
    if confirmation.lower() not in ['yes', 'y']:
        print("❌ Broadcast cancelled")
        sys.exit(0)
    
    print("\n🚀 Starting broadcast...\n")
    
    # Run broadcast
    try:
        asyncio.run(broadcast_houses_announcement())
    except KeyboardInterrupt:
        logger.info("\n⚠️ Broadcast interrupted by user")
        print("\n⚠️ Broadcast interrupted!")
    except Exception as e:
        logger.error(f"Broadcast failed with error: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
