from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

dog_types = ['terrier', 'bulldog', 'dalmatian', 'other']

def get_start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder([
        [types.InlineKeyboardButton(
            text="see all patients",
            callback_data="get_dog"
        )],
        [types.InlineKeyboardButton(
            text="find patient by pk",
            callback_data="get_dog_by_pk"
        )],
        [types.InlineKeyboardButton(
            text="add new patient",
            callback_data="create_dog"
        )],
        [types.InlineKeyboardButton(
            text="update patient info",
            callback_data="update_dog"
        )],
        [types.InlineKeyboardButton(
            text="add new timestamp entry",
            callback_data="get_post"
        )]
    ])
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_dog_type_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for dog_type in dog_types:
        kb.add(
            types.InlineKeyboardButton(
                text=f"{dog_type}",
                callback_data=f"dog_type_{dog_type}"
            )
        )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_dog_update_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder([
        [types.InlineKeyboardButton(
            text="update name",
            callback_data="update_name"
        )],
        [types.InlineKeyboardButton(
            text="update kind",
            callback_data="update_kind"
        )],
        [types.InlineKeyboardButton(
            text="complete update",
            callback_data="complete_update"
        )]
    ])
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)