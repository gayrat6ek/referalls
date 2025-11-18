"""
Subscription check handler
"""
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database import db
from keyboards import get_contact_keyboard, get_subscription_keyboard, get_main_menu_keyboard
from utils import check_user_subscription, generate_referral_link, extract_referrer_id
import logging

logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, state: FSMContext):
    """Handle subscription check callback"""
    user = callback.from_user
    user_id = user.id
    
    # Check if user is subscribed
    is_subscribed = await check_user_subscription(callback.bot, user_id)
    
    if not is_subscribed:
        # Still not subscribed
        await callback.answer(
            "❌ Siz hali kanalga obuna bo'lmadingiz. Iltimos, avval obuna bo'ling va qayta urinib ko'ring.",
            show_alert=True
        )
        return
    
    # User is subscribed
    db.update_user_subscription(user_id, True)
    await callback.answer("✅ Obuna tasdiqlandi!", show_alert=False)
    
    # Check if referral should be processed
    user_data = db.get_user(user_id)
    if user_data and user_data.get('referrer_id'):
        # Add referral if not already added
        db.add_referral(user_data['referrer_id'], user_id)
        logger.info(f"Referral processed: {user_data['referrer_id']} -> {user_id}")
    
    # Check if user has shared contact
    if not user_data.get('phone_number'):
        # Need to get contact
        await state.set_state("waiting_for_contact")
        await callback.message.edit_text(
            "✅ Ajoyib! Siz obuna bo'lgansiz.\n\n"
            "Endi aloqa ma'lumotlaringizni ulashing:"
        )
        await callback.message.answer(
            """Sizga bog'lana olishim uchun pastdagi "📲 Raqamni ulashish" tugmasini bosib telefon raqamingizni yuboring""",
            reply_markup=get_contact_keyboard()
        )
    else:
        # User is fully registered - show main menu
        referral_link = generate_referral_link(user_id)
        points = db.get_user_points(user_id)
        referral_count = db.get_referral_count(user_id)
        
        welcome_text = (
            f"✅ A'lo! Hamma narsa tayyor.\n\n"
            f"🔗 Sizning referal havolangiz:\n<code>{referral_link}</code>\n\n"
            f"📊 Statistikangiz:\n"
            f"👥 Taklif qilganlar: {referral_count}\n"
            f"⭐ Ballar: {points}\n\n"
            "Menyudan foydalaning:"
        )
        
        await callback.message.edit_text(welcome_text, parse_mode="HTML")
        await callback.message.answer(
            "Asosiy menyu:",
            reply_markup=get_main_menu_keyboard()
        )

