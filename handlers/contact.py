"""
Contact sharing handler
"""
from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import get_main_menu_keyboard
from utils import generate_referral_link
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.contact)
async def handle_contact(message: Message, state: FSMContext):
    """Handle contact sharing"""
    contact = message.contact
    user_id = message.from_user.id
    
    # Verify that user shared their own contact
    if contact.user_id != user_id:
        from keyboards import get_contact_keyboard
        await message.answer(
            "❌ Iltimos, o'zingizning aloqa ma'lumotlaringizni ulashing.",
            reply_markup=get_contact_keyboard()
        )
        return
    
    # Update user's phone number
    db.update_phone_number(user_id, contact.phone_number)
    logger.info(f"Contact saved for user {user_id}: {contact.phone_number}")
    
    # Clear state
    await state.clear()
    
    # Generate referral link
    referral_link = generate_referral_link(user_id)
    points = db.get_user_points(user_id)
    referral_count = db.get_referral_count(user_id)

    success_text = (
        "❓ Qanday qilib tanishlarni qo'shish va ball yig'ish mumkin?\n\n"
        "👥 Sizga berilgan shaxsiy havola orqali kanalga kirgan har bir tanishingiz = +1 ball.\n\n"
        "Qanchalik ko'p odam taklif qilsangiz — sovg'a yutish imkoningiz shunchalik oshadi! 🎁\n\n"
        "🔗 Do'stlarni taklif qilish uchun:\n"
        "👉 \"Shaxsiy havolam\" tugmasini bosing va tanishlaringizga yuboring.\n\n"
        "📑 Nechta odam qo'shilganini ko'rish uchun:\n"
        "👉 \"Mening ballarim\" tugmasini bosib tekshiring.\n\n"
        "Faol bo'ling — sovg'alar sizni kutyapti! 🎉\n\n"
        f"🔗 Sizning havolangiz:\n\n<code>{referral_link}</code>"
    )
    
    await message.answer(
        success_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )

