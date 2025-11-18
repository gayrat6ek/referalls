"""
Main menu handlers
"""
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
import os

from database import db
from keyboards import get_main_menu_keyboard
from utils import generate_referral_link
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "👥 Shaxsiy havolam")
async def show_referrals(message: Message):
    """Show user's referrals"""
    user_id = message.from_user.id
    referrals = db.get_user_referrals(user_id)
    referral_count = len(referrals)
    
    referral_link = generate_referral_link(user_id)
    
    text = f"""Zangiota Residence yopiq taqdimot kanaliga qo'shiling va Telfon, Muzlatgich, Televizor, Duxovka, Kir yuvish mashinasi kabi yirik sovg'alarni yutib oling! 🎁

Konkursda ishtirok etish juda oson — pastdagi havola orqali kanalga o'ting 👇👇👇

Shaxsiy havolangiz: \n\n<code>{referral_link}</code>"""
    
    # Try to send banner image with text as caption
    banner_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "banner.jpg")
    
    if os.path.exists(banner_path):
        try:
            photo = FSInputFile(banner_path)
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Error sending banner in referrals: {e}")
            # Fallback to text only
            await message.answer(text, parse_mode="HTML")
    else:
        logger.warning(f"Banner not found at {banner_path}")
        # Fallback to text only
        await message.answer(text, parse_mode="HTML")


@router.message(F.text == "⭐ Mening ballarim")
async def show_points(message: Message):
    """Show user's points"""
    user_id = message.from_user.id
    points = db.get_user_points(user_id)
    referral_count = db.get_referral_count(user_id)
    referral_link = generate_referral_link(user_id)
    text = (
        f"""📊 Mening ballarim: {points}

👥 Qo‘shilgan tanishlar soni: {referral_count}

🔥 Yana biroz harakat qiling!

Linkni yaqinlaringizga yuboring, guruhlarga ulashing — har bir qo‘shilgan odam sizni g‘oliblikka bir qadam yaqinlashtiradi! 🎁🚀

Shaxsiy havolangiz: \n\n<code>{referral_link}</code>"""
    )
    
    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "📚 Qo’llanma")
async def show_knowledge_base(message: Message):
    """Show knowledge base"""
    user_id = message.from_user.id  
    referral_link = generate_referral_link(user_id)
    
    text = f"""❓ Qanday qilib tanishlarni qo'shish va ball yig'ish mumkin?

👥 Sizga berilgan shaxsiy havola orqali kanalga kirgan har bir tanishingiz = +1 ball.

Qanchalik ko'p odam taklif qilsangiz — sovg'a yutish imkoningiz shunchalik oshadi! 🎁

🔗 Do'stlarni taklif qilish uchun:
👉 "Shaxsiy havolam" tugmasini bosing va tanishlaringizga yuboring.

📑 Nechta odam qo'shilganini ko'rish uchun:
👉 "Mening ballarim" tugmasini bosib tekshiring.

Faol bo'ling — sovg'alar sizni kutyapti! 🎉

🔗 Sizning havolangiz: \n\n{referral_link}"""
    
    await message.answer(text, parse_mode="HTML")


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    """Handle back to menu callback"""
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        "Main Menu:",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()

