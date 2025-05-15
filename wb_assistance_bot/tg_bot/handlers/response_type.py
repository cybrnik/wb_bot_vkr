# import datetime
#
# from aiogram import Router, F
# from aiogram.enums import ParseMode
# from aiogram.types import Message, CallbackQuery
# from aiogram.fsm.state import StatesGroup, State
# from aiogram.fsm.context import FSMContext
#
# from db import users_db
# from tg_bot.keyboards import patterns_made_kb
# from tg_bot.prepared_text import response_type_text
# from tg_bot import bot
#
#
# class Form(StatesGroup):
#     ai = State()
#     change_pattern = State()
#
#
# router = Router()
#
#
# @router.callback_query(lambda c: c.data == "ai")
# async def choose_ai(callback_query: CallbackQuery, state: FSMContext):
#     await users_db.add_response_type(callback_query.from_user.id, 'ai')
#     msg = await bot.send_message(callback_query.message.chat.id, response_type_text.choose_ai_text,
#                                  reply_markup=patterns_made_kb.kb3, parse_mode=ParseMode.HTML)
#     await callback_query.message.edit_text("🤖 Бот будет сам генерировать ответы на отзывы")
#     await state.set_state(Form.ai)
#     await state.update_data({'message_id': msg.message_id})
#
#
# @router.callback_query(lambda c: c.data == "about_api_start")
# async def about_api(callback_query: CallbackQuery):
#     await callback_query.message.edit_text(response_type_text.about_api_text, parse_mode=ParseMode.HTML)
#     await callback_query.message.edit_reply_markup(reply_markup=patterns_made_kb.kb4)
#
#
# @router.callback_query(lambda c: c.data == "back_to_instruction_api")
# async def back_to_instruction_api(callback_query: CallbackQuery):
#     await callback_query.message.edit_text(response_type_text.instruction_api_text, parse_mode=ParseMode.HTML)
#     await callback_query.message.edit_reply_markup(reply_markup=patterns_made_kb.kb3)
#
#
# @router.message(Form.ai)
# async def get_key(message: Message, state: FSMContext):
#     user_data = await state.get_data()
#     message_id = user_data['message_id']
#     await bot.edit_message_text(text="🔑 Ключ успешно сохранен", chat_id=message.from_user.id, message_id=message_id)
#     await users_db.add_user_key(message.from_user.id,
#                                 message.text)  # ключ в бд сохранили но еще нужна проверка работы ключа
#     current_date = datetime.datetime.now()
#     date_text = current_date.strftime("%d.%m.%Y")
#     await users_db.set_reg_date(message.from_user.id, date_text)
#     await users_db.set_activate_responses(message.from_user.id, 1)
#     await message.answer(response_type_text.get_key_text, parse_mode=ParseMode.HTML)
#     await state.clear()
#
#
# @router.callback_query(lambda c: c.data == "patterns")
# async def choose_patterns(callback_query: CallbackQuery):
#     await users_db.add_response_type(callback_query.from_user.id, 'patterns')
#     await bot.send_message(
#         callback_query.message.chat.id,
#         response_type_text.choose_patterns_text.format(
#             *[
#                 await users_db.get_pattern(callback_query.from_user.id, 'pattern{}'.format(i))
#                 for i in range(1, 6)
#             ]
#         ),
#         reply_markup=patterns_made_kb.kb1,
#         parse_mode=ParseMode.HTML
#     )
#     await callback_query.message.edit_text("📝 Бот будет отвечать на отзывы готовыми шаблонами")
#
#
# @router.callback_query(lambda c: c.data in ['1', '2', '3', '4', '5'])
# async def change_pattern(callback_query: CallbackQuery, state: FSMContext):
#     pattern_rate = 'pattern' + callback_query.data
#     await callback_query.message.edit_text(
#         response_type_text.change_pattern_text.format(
#             await users_db.get_pattern(callback_query.from_user.id, pattern_rate)),
#         reply_markup=patterns_made_kb.kb2,
#         parse_mode=ParseMode.HTML
#     )
#     await state.update_data({'pattern_number': callback_query.data, 'message_id': callback_query.message.message_id})
#     await state.set_state(Form.change_pattern)
#
#
# @router.callback_query(lambda c: c.data == "back_to_patterns")
# async def choose_patterns(callback_query: CallbackQuery):
#     await callback_query.message.edit_text(
#         response_type_text.choose_patterns_text.format(
#             *[
#                 await users_db.get_pattern(callback_query.from_user.id, 'pattern{}'.format(i))
#                 for i in range(1, 6)
#             ]
#         ),
#         parse_mode=ParseMode.HTML
#     )
#     await callback_query.message.edit_reply_markup(reply_markup=patterns_made_kb.kb1)
#
#
# @router.message(Form.change_pattern)
# async def get_new_pattern(message: Message, state: FSMContext):
#     state_data = await state.get_data()
#     pattern_rate = "pattern" + str(state_data['pattern_number'])
#     await users_db.set_patterns(message.from_user.id, pattern_rate, message.text)
#     await message.delete()
#     message_to_edit = state_data['message_id']
#     await bot.edit_message_text(
#         chat_id=message.chat.id,
#         message_id=message_to_edit,
#         text=response_type_text.choose_patterns_text.format(
#             *[
#                 await users_db.get_pattern(message.from_user.id, 'pattern{}'.format(i))
#                 for i in range(1, 6)
#             ]
#         ),
#         parse_mode=ParseMode.HTML
#     )
#     await bot.edit_message_reply_markup(chat_id=message.chat.id, message_id=message_to_edit,
#                                         reply_markup=patterns_made_kb.kb1)
#     await state.clear()
#
#
# @router.callback_query(lambda c: c.data == "patterns_done")
# async def patterns_done(callback_query: CallbackQuery, state: FSMContext):
#     await callback_query.message.delete()
#     msg = await bot.send_message(
#         callback_query.message.chat.id,
#         response_type_text.patterns_done_text,
#         reply_markup=patterns_made_kb.kb3,
#         parse_mode=ParseMode.HTML
#     )
#     await state.set_state(Form.ai)
#     await state.update_data({'message_id': msg.message_id})
