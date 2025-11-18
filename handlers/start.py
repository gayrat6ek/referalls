"""
Start command handler
"""
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
import os

from database import db
from keyboards import get_subscription_keyboard, get_main_menu_keyboard
from utils import check_user_subscription, extract_referrer_id, generate_referral_link
import logging

logger = logging.getLogger(__name__)

router = Router()

# Welcome message text
WELCOME_TEXT = """🎉 Zangiota Residence aksiyasida ishtirok etayotganingizdan mamnunmiz!

Do'stlaringizni kanalga taklif qilib, katta va qimmatbaho sovg'alarni yutib olishingiz mumkin!

Keling, qisqacha tushuntiramiz 👇

⸻

👉 Eng ko'p odam taklif qilgan ishtirokchi
🎁 Bizdagi yirik sovg'alardan xohlagan birini o'zi tanlab oladi:
 • Telefon
 • Duxovka
 • Xolodilnik
 • Televizor
 • Kir yuvish mashinasi

⸻

👉 Barcha faol ishtirokchilar orasidan
🎁 Tasodifiy tarzda sovg'alar o'ynaladi — hech kim e'tiborsiz qolmaydi.
Taklif qilganlarning har biri sovg'a olish imkoniga ega.

⸻

📅 G'oliblar 21-noyabrdan boshlab, hammaning ko'zi oldida, onlayn tarzda aniqlanadi."""


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    """Handle /start command"""
    user = message.from_user
    user_id = user.id
    
    # Extract referrer ID from deep link
    args = message.text.split(maxsplit=1)
    referrer_id = None
    
    if len(args) > 1:
        start_param = args[1]
        referrer_id = extract_referrer_id(start_param)
        
        # Don't allow self-referral
        if referrer_id == user_id:
            referrer_id = None
    
    # Add user to database
    existing_user = db.get_user(user_id)
    
    if not existing_user:
        # New user
        db.add_user(
            user_id=user_id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            referrer_id=referrer_id
        )
        logger.info(f"New user registered: {user_id} (referrer: {referrer_id})")
    else:
        # Existing user - update info if needed
        logger.info(f"Existing user: {user_id}")
    
    # Check subscription status
    is_subscribed = await check_user_subscription(message.bot, user_id)
    
    if not is_subscribed:
        # User not subscribed - show banner with welcome message first
        banner_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "banner.jpg")
        
        if os.path.exists(banner_path):
            try:
                photo = FSInputFile(banner_path)
                await message.answer_photo(
                    photo=photo,
                    caption=WELCOME_TEXT
                )
            except Exception as e:
                logger.error(f"Error sending banner: {e}")
                # Fallback to text only
                await message.answer(WELCOME_TEXT)
        else:
            logger.warning(f"Banner not found at {banner_path}")
            # Fallback to text only
            await message.answer(WELCOME_TEXT)
        
        # Then show subscription message with buttons
        subscription_text = (
            "⬇️ Aksiyada ishtirok etish uchun avval kanalimizga obuna bo'ling.\n\n"
            "Quyidagi tugmani bosing va obuna bo'lgandan keyin "
            "\"✅ Obunani Tekshirish\" tugmasini bosing."
        )
        await message.answer(
            subscription_text,
            reply_markup=get_subscription_keyboard()
        )
    else:
        # User is subscribed
        db.update_user_subscription(user_id, True)
        
        # If user came via referral link and it's their first subscription
        if referrer_id and not existing_user:
            db.add_referral(referrer_id, user_id)
            logger.info(f"Referral added: {referrer_id} -> {user_id}")
        
        # Check if user has shared contact
        user_data = db.get_user(user_id)
        if not user_data.get('phone_number'):
            # Need to get contact
            await state.set_state("waiting_for_contact")
            from keyboards import get_contact_keyboard
            await message.answer(
                """Sizga bog'lana olishim uchun pastdagi "📲 Raqamni ulashish" tugmasini bosib telefon raqamingizni yuboring""",
                reply_markup=get_contact_keyboard()
            )
        else:
            # User is fully registered - show main menu
            referral_link = generate_referral_link(user_id)
            points = db.get_user_points(user_id)
            referral_count = db.get_referral_count(user_id)
            welcome_back_text = f"""📊 Mening ballarim: {points}

👥 Qo‘shilgan tanishlar soni: {referral_count}

🔥 Yana biroz harakat qiling!

Linkni yaqinlaringizga yuboring, guruhlarga ulashing — har bir qo‘shilgan odam sizni g‘oliblikka bir qadam yaqinlashtiradi! 🎁🚀

Shaxsiy havolangiz: \n\n{referral_link}"""
            
            
            await message.answer(
                welcome_back_text,
                reply_markup=get_main_menu_keyboard(),
                parse_mode="HTML"
            )

