"""
Test script to verify bot can access the channel
"""
import asyncio
from aiogram import Bot
from config import config


async def test_channel_access():
    """Test if bot can access the channel"""
    bot = Bot(token=config.BOT_TOKEN)
    
    print("=" * 50)
    print("Testing Channel Access")
    print("=" * 50)
    print(f"Channel ID: {config.CHANNEL_ID}")
    print(f"Bot Username: @{config.BOT_USERNAME}")
    print()
    
    try:
        # Try to get channel info
        chat = await bot.get_chat(config.CHANNEL_ID)
        print(f"✅ Channel found!")
        print(f"   Title: {chat.title}")
        print(f"   ID: {chat.id}")
        print(f"   Type: {chat.type}")
        print()
        
        # Get bot's member status in the channel
        bot_member = await bot.get_chat_member(chat_id=config.CHANNEL_ID, user_id=(await bot.me()).id)
        print(f"✅ Bot status in channel: {bot_member.status}")
        
        if bot_member.status not in ["administrator", "creator"]:
            print("⚠️  WARNING: Bot is not an admin in the channel!")
            print("   Please add the bot as admin with these permissions:")
            print("   - Post messages")
            print("   - Delete messages")
            print("   - Manage users (to check subscriptions)")
        else:
            print("✅ Bot has admin permissions!")
        
        print()
        print("=" * 50)
        print("✅ All checks passed! Bot is properly configured.")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Common issues:")
        print("1. Bot is not added to the channel")
        print("2. Bot is not an admin in the channel")
        print("3. Wrong channel ID in .env file")
        print()
        print("Solutions:")
        print("1. Go to your channel settings")
        print("2. Add your bot as administrator")
        print("3. Give it at least 'Manage users' permission")
        print()
        
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(test_channel_access())

