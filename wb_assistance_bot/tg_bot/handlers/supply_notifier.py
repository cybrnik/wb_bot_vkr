from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from wb_assistance_bot.db.users import users_db
from wb_assistance_bot.tg_bot.bot import bot
import wb_assistance_bot.tg_bot.keyboards.supply_notifier_kb as supply_notifier_kb
import wb_assistance_bot.tg_bot.prepared_text.supply_notifier as supply_notifier_text

router = Router()


class Form(StatesGroup):
    wait_for_key_statistics = State()


@router.message(Command("supply_notifier"))
async def supply_notifier(message: Message):
    await message.answer(supply_notifier_text.info_text,
                         reply_markup=supply_notifier_kb.kb,
                         parse_mode=ParseMode.HTML)


@router.callback_query(lambda c: c.data == "close_supply_notifier")
async def close_supply_notifier(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await state.clear()


@router.callback_query(lambda c: c.data == "change_api_statistics_key")
async def close_supply_notifier(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(supply_notifier_text.instruction_api_after_reg_text,
                                           parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=supply_notifier_kb.kb1)
    await state.update_data({'message_id': callback_query.message.message_id})
    await state.set_state(Form.wait_for_key_statistics)


@router.message(Form.wait_for_key_statistics)
async def change_key(message: Message, state: FSMContext):
    await users_db.set_statistics_api(message.from_user.id,
                                      message.text)
    state_data = await state.get_data()
    await bot.edit_message_text(chat_id=message.chat.id, message_id=state_data['message_id'],
                                text="Ключ успешно сохранен")
    await message.delete()
    await state.clear()


@router.callback_query(lambda c: c.data == "about_api_supplies")
async def about_api(callback_query: CallbackQuery):
    await callback_query.message.edit_text(supply_notifier_text.about_api_text, parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=supply_notifier_kb.kb2)


@router.callback_query(lambda c: c.data == "back_to_api_instruction")
async def about_api(callback_query: CallbackQuery):
    await callback_query.message.edit_text(supply_notifier_text.instruction_api_after_reg_text,
                                           parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=supply_notifier_kb.kb1)


@router.callback_query(lambda c: c.data == "back_to_settings_supplies")
async def about_api(callback_query: CallbackQuery):
    await callback_query.message.edit_text(supply_notifier_text.info_text, parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=supply_notifier_kb.kb)
