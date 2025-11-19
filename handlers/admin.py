"""
Admin command handlers
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from datetime import datetime
import io

from database import db
from config import config
import logging

logger = logging.getLogger(__name__)

router = Router()


def is_admin(user_id: int) -> bool:
    """Check if user is admin"""
    return user_id == config.ADMIN_USER_ID


@router.message(Command("stats"))
async def cmd_stats(message: Message):
    """Show bot statistics (admin only) - Send as file"""
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await message.answer("⛔ Bu buyruq faqat administratorlar uchun.")
        logger.warning(f"Unauthorized stats access attempt by user {user_id}")
        return
    
    await message.answer("📊 Statistika tayyorlanmoqda...")
    
    # Gather statistics
    total_users = db.get_total_users()
    total_referrals = db.get_total_referrals()
    subscribed_users = db.get_subscribed_users_count()
    users_with_phone = db.get_users_with_phone_count()
    top_referrers = db.get_top_referrers(limit=50)
    
    # Build statistics text
    stats_text = "=" * 50 + "\n"
    stats_text += "📊 BOT STATISTIKASI\n"
    stats_text += "=" * 50 + "\n\n"
    
    stats_text += "📈 UMUMIY STATISTIKA\n"
    stats_text += "-" * 50 + "\n"
    stats_text += f"👥 Jami foydalanuvchilar:        {total_users}\n"
    stats_text += f"✅ Obuna bo'lganlar:              {subscribed_users}\n"
    stats_text += f"📱 Telefon ulashganlar:           {users_with_phone}\n"
    stats_text += f"🔗 Jami referal havolalar:        {total_referrals}\n\n"
    
    if total_users > 0:
        subscription_rate = (subscribed_users / total_users) * 100
        phone_rate = (users_with_phone / total_users) * 100
        stats_text += f"📊 Obuna darajasi:                {subscription_rate:.1f}%\n"
        stats_text += f"📊 Telefon ulashish darajasi:     {phone_rate:.1f}%\n\n"
    
    # Top referrers
    stats_text += "=" * 50 + "\n"
    stats_text += "🏆 TOP 50 REFERALCHILAR\n"
    stats_text += "=" * 50 + "\n\n"
    
    if top_referrers:
        for idx, referrer in enumerate(top_referrers, 1):
            user_id_ref = referrer.get('user_id', 'N/A')
            name = referrer.get('first_name', 'Noma\'lum')
            username = referrer.get('username', 'username yo\'q')
            phone = referrer.get('phone_number', 'telefon yo\'q')
            ref_count = referrer.get('referral_count', 0)
            points = referrer.get('points', 0)
            
            stats_text += f"{idx}. {name} (@{username})\n"
            stats_text += f"   User ID: {user_id_ref}\n"
            stats_text += f"   📱 Telefon: {phone}\n"
            stats_text += f"   👥 Takliflar: {ref_count}\n"
            stats_text += f"   ⭐ Ballar: {points}\n"
            stats_text += "-" * 50 + "\n"
    else:
        stats_text += "Hozircha referallar yo'q.\n\n"
    
    stats_text += "\n" + "=" * 50 + "\n"
    stats_text += f"🕐 Yaratilgan vaqt: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    stats_text += "=" * 50 + "\n"
    
    # Create file in memory
    file_content = stats_text.encode('utf-8')
    file_name = f"bot_stats_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Send as document
    document = BufferedInputFile(file_content, filename=file_name)
    await message.answer_document(
        document=document,
        caption=f"📊 Bot statistikasi\n🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    
    logger.info(f"Stats file sent to admin {user_id}")



@router.message(Command("admin"))
async def cmd_admin(message: Message):
    """Show admin commands"""
    user_id = message.from_user.id
    
    if not is_admin(user_id):
        await message.answer("⛔ Bu buyruq faqat administratorlar uchun.")
        return
    
    admin_text = (
        "🔧 **ADMIN BUYRUQLARI**\n\n"
        "/stats - Bot statistikasini ko'rish\n"
        "/admin - Admin buyruqlar ro'yxati\n"
    )
    
    await message.answer(admin_text, parse_mode="Markdown")

