"""
Keyboard layouts for the bot
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from config import config


def get_subscription_keyboard() -> InlineKeyboardMarkup:
    """Get inline keyboard for channel subscription"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➕KANALGA OBUNA BO’LISH", url=config.CHANNEL_LINK)],
        [InlineKeyboardButton(text="Bajarildi ✅", callback_data="check_subscription")]
    ])
    return keyboard


def get_contact_keyboard() -> ReplyKeyboardMarkup:
    """Get reply keyboard for requesting contact"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📲 Raqamni ulashish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu reply keyboard"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Shaxsiy havolam"), KeyboardButton(text="⭐ Mening ballarim")],
            [KeyboardButton(text="📚 Qo’llanma")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Get inline keyboard with back to menu button"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Back to Menu", callback_data="back_to_menu")]
    ])
    return keyboard

