"""
Admin command handlers
"""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
from datetime import datetime
from zoneinfo import ZoneInfo
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
    
    # Get current time in Uzbekistan timezone
    uz_time = datetime.now(ZoneInfo("Asia/Tashkent"))
    
    stats_text += "\n" + "=" * 50 + "\n"
    stats_text += f"🕐 Yaratilgan vaqt: {uz_time.strftime('%Y-%m-%d %H:%M:%S')} (UZT)\n"
    stats_text += "=" * 50 + "\n"
    
    # Create file in memory
    file_content = stats_text.encode('utf-8')
    file_name = f"bot_stats_{uz_time.strftime('%Y%m%d_%H%M%S')}.txt"
    
    # Send as document
    document = BufferedInputFile(file_content, filename=file_name)
    await message.answer_document(
        document=document,
        caption=f"📊 Bot statistikasi\n🕐 {uz_time.strftime('%Y-%m-%d %H:%M:%S')} (UZT)"
    )
    
    logger.info(f"Stats file sent to admin {user_id}")



@router.message(Command("users"))
async def cmd_users(message: Message):
    """Show users with referrals (admin only) - Send as file"""
    user_id = message.from_user.id
    
    # Check if user is admin
    if not is_admin(user_id):
        await message.answer("⛔ Bu buyruq faqat administratorlar uchun.")
        logger.warning(f"Unauthorized users access attempt by user {user_id}")
        return
    
    await message.answer("👥 Foydalanuvchilar ro'yxati tayyorlanmoqda...")
    
    # Get users with referrals
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                u.user_id,
                u.first_name,
                u.last_name,
                u.username,
                u.phone_number,
                COUNT(r.id) as referral_count
            FROM users u
            INNER JOIN referrals r ON u.user_id = r.referrer_id
            GROUP BY u.user_id, u.first_name, u.last_name, u.username, u.phone_number
            HAVING referral_count >= 1
            ORDER BY referral_count DESC, u.first_name ASC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        # Build users text
        users_text = "=" * 70 + "\n"
        users_text += "👥 REFERALI FOYDALANUVCHILAR\n"
        users_text += "=" * 70 + "\n\n"
        
        if rows:
            users_text += f"Jami foydalanuvchilar: {len(rows)}\n"
            users_text += "=" * 70 + "\n\n"
            
            # Calculate statistics
            total_referrals = sum(row['referral_count'] for row in rows)
            avg_referrals = total_referrals / len(rows) if rows else 0
            max_referrals = max((row['referral_count'] for row in rows), default=0)
            
            users_text += f"📊 STATISTIKA:\n"
            users_text += f"   • Jami referalli foydalanuvchilar: {len(rows)}\n"
            users_text += f"   • Jami taklif qilinganlar: {total_referrals}\n"
            users_text += f"   • O'rtacha taklif (har bir foydalanuvchi): {avg_referrals:.2f}\n"
            users_text += f"   • Maksimal taklif (bitta foydalanuvchi): {max_referrals}\n\n"
            users_text += "=" * 70 + "\n\n"
            
            # Add user details
            for idx, row in enumerate(rows, 1):
                # Construct full name
                full_name = ""
                if row['first_name']:
                    full_name += row['first_name']
                if row['last_name']:
                    full_name += f" {row['last_name']}"
                if not full_name:
                    full_name = f"User {row['user_id']}"
                
                username = row['username'] or "username yo'q"
                phone = row['phone_number'] or "telefon yo'q"
                ref_count = row['referral_count']
                
                users_text += f"{idx}. {full_name}\n"
                users_text += f"   User ID: {row['user_id']}\n"
                users_text += f"   Username: @{username}\n"
                users_text += f"   📱 Telefon: {phone}\n"
                users_text += f"   👥 Takliflar soni: {ref_count}\n"
                users_text += "-" * 70 + "\n"
        else:
            users_text += "Hozircha referal qilgan foydalanuvchilar yo'q.\n\n"
        
        # Get current time in Uzbekistan timezone
        uz_time = datetime.now(ZoneInfo("Asia/Tashkent"))
        
        users_text += "\n" + "=" * 70 + "\n"
        users_text += f"🕐 Yaratilgan vaqt: {uz_time.strftime('%Y-%m-%d %H:%M:%S')} (UZT)\n"
        users_text += "=" * 70 + "\n"
        
        # Create file in memory
        file_content = users_text.encode('utf-8')
        file_name = f"users_with_referrals_{uz_time.strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Send as document
        document = BufferedInputFile(file_content, filename=file_name)
        await message.answer_document(
            document=document,
            caption=f"👥 Referali foydalanuvchilar ro'yxati\n🕐 {uz_time.strftime('%Y-%m-%d %H:%M:%S')} (UZT)"
        )
        
        logger.info(f"Users list file sent to admin {user_id}")
        
    except Exception as e:
        logger.error(f"Error generating users list: {e}")
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")


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
        "/users - Referalli foydalanuvchilar ro'yxati\n"
        "/admin - Admin buyruqlar ro'yxati\n"
    )
    
    await message.answer(admin_text, parse_mode="Markdown")

