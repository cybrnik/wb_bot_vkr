from aiogram import Router, F, Bot
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hbold

from wb_assistance_bot.db import users_db
from wb_assistance_bot.tg_bot.keyboards import feedbacks_settings_kb
from wb_assistance_bot.tg_bot.prepared_text import response_type_text
from wb_assistance_bot.tg_bot import bot

router = Router()


class Form(StatesGroup):
    change_pattern1 = State()
    wait_for_key = State()


@router.message(Command("auto_feedback"))
async def response_settings(message: Message, state: FSMContext):
    if await users_db.get_activate_responses(message.from_user.id) == 1:
        if await users_db.get_response_type(message.from_user.id) == 'patterns':
            await message.answer("Сейчас бот отвечает на отзывы шаблонами", reply_markup=feedbacks_settings_kb.kb)
        else:
            await message.answer("Сейчас бот сам генерирует ответы на отзывы",
                                 reply_markup=feedbacks_settings_kb.kb4)
        await state.clear()
    else:
        await message.answer("Сейчас бот не отвечает на отзывы", reply_markup=feedbacks_settings_kb.kb7)


@router.callback_query(lambda c: c.data == "see_patterns")
async def see_patterns(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        response_type_text.choose_patterns_text.format(
            *[
                await users_db.get_pattern(callback_query.from_user.id, 'pattern{}'.format(i))
                for i in range(1, 6)
            ]
        ),
        parse_mode=ParseMode.HTML
    )
    await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb1)


@router.callback_query(lambda c: c.data == "back_to_feedback_settings")
async def show_feedback_settings(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Сейчас я отвечаю на отзывы шаблонами")
    await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb)
    await state.clear()


@router.callback_query(lambda c: c.data in ['edit1', 'edit2', 'edit3', 'edit4', 'edit5'])
async def change_pattern(callback_query: CallbackQuery, state: FSMContext):
    pattern_rate = 'pattern' + callback_query.data[-1]
    await callback_query.message.edit_text(
        "Отправьте ответным сообщением новый текст ответа, если хотите заменить текущий\n\n"
        "Текущий текст ответа:\n\n"
        f"{await users_db.get_pattern(callback_query.from_user.id, pattern_rate)}",
        reply_markup=feedbacks_settings_kb.kb3,
        parse_mode=ParseMode.HTML)
    await state.update_data({'pattern_number': callback_query.data, 'message_id': callback_query.message.message_id})
    await state.set_state(Form.change_pattern1)


@router.message(Form.change_pattern1)
async def get_new_pattern(message: Message, state: FSMContext):
    state_data = await state.get_data()
    pattern_rate = "pattern" + str(state_data['pattern_number'][-1])
    await users_db.set_patterns(message.from_user.id, pattern_rate, message.text)
    await message.delete()
    message_to_edit = state_data['message_id']
    await bot.edit_message_text(
        chat_id=message.chat.id, message_id=message_to_edit,
        text=response_type_text.choose_patterns_text.format(
            *[
                await users_db.get_pattern(message.from_user.id, 'pattern{}'.format(i))
                for i in range(1, 6)
            ]
        ),
        parse_mode=ParseMode.HTML
    )
    await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_to_edit,
                                        reply_markup=feedbacks_settings_kb.kb1)
    await state.clear()


@router.callback_query(lambda c: c.data == "close_feedbacks_settings")
async def close_feedback_settings(callback_query: CallbackQuery):
    await callback_query.message.delete()


@router.callback_query(lambda c: c.data == "change_response_type_to_ai")
async def change_response_to_api(callback_query: CallbackQuery, state: FSMContext):
    await users_db.set_response_type(callback_query.from_user.id, 'ai')
    await callback_query.message.edit_text("Сейчас бот сам генерирует ответы на отзывы",
                                           reply_markup=feedbacks_settings_kb.kb4,
                                           parse_mode=ParseMode.HTML)
    await state.clear()


@router.callback_query(lambda c: c.data == "change_response_type_to_patterns")
async def change_response_type_to_patterns(callback_query: CallbackQuery):
    await users_db.set_response_type(callback_query.from_user.id, 'patterns')
    await callback_query.message.edit_text("Сейчас бот отвечает на отзывы шаблонами",
                                           reply_markup=feedbacks_settings_kb.kb)


@router.callback_query(lambda c: c.data == "change_api_key")
async def change_api_key(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(response_type_text.instruction_api_after_reg_text,
                                           parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb5)
    await state.update_data({'message_id': callback_query.message.message_id})
    await state.set_state(Form.wait_for_key)


@router.callback_query(lambda c: c.data == "back_to_settings")
async def back_to_settings(callback_query: CallbackQuery, state: FSMContext):
    if await users_db.get_response_type(callback_query.from_user.id) == 'patterns':
        await callback_query.message.edit_text("Сейчас бот отвечает на отзывы шаблонами")
        await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb)
    else:
        await callback_query.message.edit_text("Сейчас бот сам генерирует ответы на отзывы")
        await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb4)
    await state.clear()


@router.callback_query(lambda c: c.data == "about_api")
async def about_api(callback_query: CallbackQuery):
    await callback_query.message.edit_text(response_type_text.about_api_text, parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb6)


@router.message(Form.wait_for_key)
async def change_key(message: Message, state: FSMContext):
    await users_db.set_api_feedbacks(message.from_user.id,
                                     message.text)
    state_data = await state.get_data()
    if await users_db.get_response_type(message.from_user.id) == 'patterns':
        await message.answer("Ключ сохранен")
        await bot.edit_message_text(chat_id=message.chat.id, message_id=state_data['message_id'],
                                    text="Сейчас бот отвечает на отзывы шаблонами")
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=state_data['message_id'],
                                            reply_markup=feedbacks_settings_kb.kb)
    else:
        await message.answer("Ключ сохранен")
        await bot.edit_message_text(chat_id=message.chat.id, message_id=state_data['message_id'],
                                    text="Сейчас бот сам генерирует ответы на отзывы")
        await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=state_data['message_id'],
                                            reply_markup=feedbacks_settings_kb.kb4)
    await message.delete()
    await state.clear()


@router.callback_query(lambda c: c.data == "stop_responses")
async def stop_making_responses(callback_query: CallbackQuery):
    await users_db.set_activate_responses(callback_query.from_user.id, 0)
    await callback_query.message.edit_text("Сейчас бот не отвечает на отзывы")
    await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb7)


@router.callback_query(lambda c: c.data == "continue_feedbacks")
async def continue_making_responses(callback_query: CallbackQuery):
    await users_db.set_activate_responses(callback_query.from_user.id, 1)
    if await users_db.get_response_type(callback_query.from_user.id) == 'patterns':
        await callback_query.message.edit_text("Сейчас бот отвечает на отзывы шаблонами")
        await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb)
    else:
        await callback_query.message.edit_text("Сейчас бот сам генерирует ответы на отзывы")
        await callback_query.message.edit_reply_markup(reply_markup=feedbacks_settings_kb.kb4)
