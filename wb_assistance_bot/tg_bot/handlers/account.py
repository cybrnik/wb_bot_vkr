from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from wb_assistance_bot.db import users_db
from wb_assistance_bot.tg_bot.keyboards import account_kb
from wb_assistance_bot.tg_bot.keyboards import feedbacks_settings_kb
from wb_assistance_bot.tg_bot import bot
from wb_assistance_bot.tg_bot.prepared_text import account_text

router = Router()


@router.message(Command("account"))
async def account(message: Message):
    active = await users_db.get_activate_responses(message.from_user.id)
    needed_text = ""
    if await users_db.get_response_type(message.from_user.id) == "ai":
        if active == 1:
            needed_text = account_text.get_ai_lk_text(await users_db.get_num_responses(message.from_user.id))
    else:
        if active == 1:
            needed_text = account_text.get_no_ai_lk_text(await users_db.get_num_responses(message.from_user.id))
    if active == 0:
        needed_text = account_text.not_making_responses(await users_db.get_num_responses(message.from_user.id))

    feedbacks_key = await users_db.get_api_feedbacks(message.from_user.id)
    supplies_key = await users_db.get_statistics_api(message.from_user.id)
    financial_key = await users_db.get_finance_api(message.from_user.id)
    advertising_key = await users_db.get_api_advertising(message.from_user.id)

    feedbacks_text = ""
    supplies_text = ""
    financial_text = ""
    advertising_text = ""

    if (feedbacks_key != "new_user") and (feedbacks_key != "incorrect_api"):
        feedbacks_text = "✅Ключ для работы с отзывами предоставлен"
    else:
        feedbacks_text = "❌Ключ для работы с отзывами не предоставлен"

    if (supplies_key != "new_user") and (supplies_key != "incorrect_api"):
        supplies_text = "✅Ключ для работы с поставками предоставлен"
    else:
        supplies_text = "❌Ключ для работы с поставками не предоставлен"

    if (financial_key != "new_user") and (financial_key != "incorrect_api"):
        financial_text = "✅Ключ для работы с финансами предоставлен"
    else:
        financial_text = "❌Ключ для работы с финансами не предоставлен"

    if (advertising_key != "new_user") and (advertising_key != "incorrect_api"):
        advertising_text = "✅Ключ для работы с рекламой предоставлен"
    else:
        advertising_text = "❌Ключ для работы с финансами не предоставлен"

    await message.answer(
        text=needed_text + "\n" + feedbacks_text + "\n\n" + supplies_text + "\n\n" + financial_text + "\n\n" + advertising_text,
        parse_mode=ParseMode.HTML,
        reply_markup=account_kb.kb
    )


@router.callback_query(lambda c: c.data == "feedbacks_settings")
async def feedbacks_settings(callback_query: CallbackQuery):
    await callback_query.message.delete()
    await bot.answer_callback_query(callback_query.id)

    if await users_db.get_activate_responses(callback_query.from_user.id) == 1:
        if await users_db.get_response_type(callback_query.from_user.id) == 'patterns':
            await bot.send_message(callback_query.message.chat.id, "Сейчас бот отвечает на отзывы шаблонами",
                                   reply_markup=feedbacks_settings_kb.kb)
        else:
            await bot.send_message(callback_query.message.chat.id, "Сейчас бот сам генерирует ответы на отзывы",
                                   reply_markup=feedbacks_settings_kb.kb4)
    else:
        await bot.send_message(callback_query.message.chat.id, "Сейчас бот не отвечает на отзывы",
                               reply_markup=account_kb.kb2)
