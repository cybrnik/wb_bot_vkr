import os

import pandas as pd
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import datetime

from wb_assistance_bot.db import users_db
from wb_assistance_bot.tg_bot.prepared_text import start_handler_text
from wb_assistance_bot.tg_bot.keyboards import start_kb
from aiogram.fsm.state import StatesGroup, State
from wb_assistance_bot.tg_bot import bot
from openpyxl import load_workbook

router = Router()


class Form(StatesGroup):
    getting_tax_rate = State()


@router.message(Command("start"))
async def start(message: Message, state: FSMContext) -> None:
    if not os.path.exists('prod_costs'):
        os.makedirs('prod_costs')
    user_id = message.from_user.id
    file_path = os.path.join('prod_costs', f'{user_id}.xlsx')
    columns = ['Артикул поставщика', 'Артикул WB', 'Себестоимость']
    df = pd.DataFrame(columns=columns)
    df.to_excel(file_path, index=False)
    wb = load_workbook(file_path)
    ws = wb.active
    column_widths = {
        'A': 25,  # артикул поставщика
        'B': 20,  # артикул WB
        'C': 15  # себестоимость
    }
    for col_letter, width in column_widths.items():
        ws.column_dimensions[col_letter].width = width
    wb.save(file_path)
    username = message.from_user.username
    await users_db.add_user(user_id, username)

    await users_db.set_patterns(user_id, 'pattern1',
                                "Нам очень жаль, что Вам не понравился товар. Мы обязательно предпримем меры и будем работать над улучшением качества нашего продукта")
    await users_db.set_patterns(user_id, 'pattern2',
                                "Спасибо за Ваш отзыв. Мы приносим извинения, если наш продукт не соответсвует Вашим ожиданиям")
    await users_db.set_patterns(user_id, 'pattern3',
                                "Спасибо за Ваш отзыв. Мы ценим обратную связь и будем работать над улучшением нашего продукта еще больше")
    await users_db.set_patterns(user_id, 'pattern4',
                                "Спасибо за уделенное время на отзыв. Мы очень рады, что Вам понравился наш продукт и обязательно продолжим работать над улучшением его качества")
    await users_db.set_patterns(user_id, 'pattern5',
                                "Спасибо за уделенное время на отзыв. Мы очень рады, что Вам понравился наш продукт! Хорошего настроения!")

    current_date = datetime.datetime.now()
    date_text = current_date.strftime("%d.%m.%Y")
    await users_db.set_reg_date(message.from_user.id, date_text)
    await message.answer(start_handler_text.start_text, parse_mode=ParseMode.HTML, reply_markup=start_kb.kb1)


@router.callback_query(lambda c: c.data == "tax_system")
async def reg_tax_system(callback_query: CallbackQuery):
    await callback_query.message.edit_text(start_handler_text.reg_tax_system, parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=start_kb.kb2)


@router.callback_query(lambda c: c.data == "incomes")
async def reg_tax_system1(callback_query: CallbackQuery, state: FSMContext):
    await users_db.set_tax_system(callback_query.from_user.id, "incomes")
    await callback_query.message.edit_text(start_handler_text.reg_tax_rate, parse_mode=ParseMode.HTML)
    await state.update_data({'message_id': callback_query.message.message_id})
    await state.set_state(Form.getting_tax_rate)


@router.callback_query(lambda c: c.data == "incomes_expenses")
async def reg_tax_system2(callback_query: CallbackQuery, state: FSMContext):
    await users_db.set_tax_system(callback_query.from_user.id, "incomes_expenses")
    await callback_query.message.edit_text(start_handler_text.reg_tax_rate, parse_mode=ParseMode.HTML)
    await state.update_data({'message_id': callback_query.message.message_id})
    await state.set_state(Form.getting_tax_rate)


@router.message(Form.getting_tax_rate)
async def tax_rate_processing(message: Message, state: FSMContext):
    state_data = await state.get_data()
    mes_id = state_data['message_id']
    mes_text = message.text
    if mes_text.isdigit():
        tax_rate = int(mes_text)
        await users_db.set_tax_rate(message.from_user.id, tax_rate)
        await bot.delete_message(chat_id=message.chat.id, message_id=state_data['message_id'])
        await message.delete()
        await bot.send_message(chat_id=message.chat.id,
                               text="Налоговая ставка успешно сохранена\n\nДля дальнейшей работы выберите раздел в Menu")
        await state.clear()
    else:
        if mes_text.__contains__("%"):
            text = mes_text.replace("%", "")
            if text.isdigit():
                tax_rate = int(text)
                await users_db.set_tax_rate(message.from_user.id, tax_rate)
                await bot.delete_message(chat_id=message.chat.id, message_id=state_data['message_id'])
                await message.delete()
                await bot.send_message(chat_id=message.chat.id,
                                       text="Налоговая ставка успешно сохранена\n\nДля дальнейшей работы выберите раздел в Menu")
                await state.clear()
            else:
                await bot.send_message(chat_id=message.chat.id, text="Некорректно введена налоговая ставка")
        else:
            await bot.send_message(chat_id=message.chat.id, text="Некорректно введена налоговая ставка")
