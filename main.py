"""
Main bot entry point
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import start, subscription, contact, menu, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main function to start the bot"""
    # Validate configuration
    if config.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        logger.error("Bot token not configured! Please set BOT_TOKEN in environment or config.py")
        sys.exit(1)
    
    if config.CHANNEL_ID == "@your_channel":
        logger.warning("Channel ID not configured! Please set CHANNEL_ID in environment or config.py")
    
    # Initialize bot and dispatcher
    bot = Bot(
        token=config.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher(storage=MemoryStorage())
    
    # Register routers
    dp.include_router(admin.router)  # Admin router first for priority
    dp.include_router(start.router)
    dp.include_router(subscription.router)
    dp.include_router(contact.router)
    dp.include_router(menu.router)
    
    logger.info("Bot starting...")
    
    try:
        # Start polling
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped with error: {e}")
        sys.exit(1)

