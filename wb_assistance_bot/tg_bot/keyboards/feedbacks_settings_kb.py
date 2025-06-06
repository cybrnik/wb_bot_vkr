from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = InlineKeyboardBuilder()
kb.button(text="📄Текущие шаблоны", callback_data='see_patterns')
kb.button(text="🤖Сменить систему ответов на отзывы", callback_data='change_response_type_to_ai')
kb.button(text="✍️Сменить API ключ", callback_data='change_api_key')
kb.button(text="⛔️Остановить автоответы", callback_data="stop_responses")
kb.button(text="✖️Закрыть", callback_data='close_feedbacks_settings')
kb.adjust(1)
kb = kb.as_markup()

kb1 = InlineKeyboardBuilder()
kb1.button(text="⭐️", callback_data="edit1")
kb1.button(text="⭐⭐️️", callback_data="edit2")
kb1.button(text="⭐️⭐️⭐️", callback_data="edit3")
kb1.button(text="⭐️⭐️⭐️⭐️", callback_data="edit4")
kb1.button(text="⭐️⭐️⭐️⭐️⭐️", callback_data="edit5")
kb1.button(text="Вернуться назад", callback_data="back_to_feedback_settings")
kb1.adjust(1)
kb1 = kb1.as_markup()

kb2 = InlineKeyboardBuilder()
kb2.button(text="Вернуться назад", callback_data="back_to_patterns_in_settings")
kb2 = kb2.as_markup()

kb3 = InlineKeyboardBuilder()
kb3.button(text="Вернуться назад", callback_data="see_patterns")
kb3 = kb3.as_markup()

kb4 = InlineKeyboardBuilder()
kb4.button(text="📄Сменить систему ответов на отзывы", callback_data='change_response_type_to_patterns')
kb4.button(text="✍️Сменить API ключ", callback_data='change_api_key')
kb4.button(text="⛔️Остановить автоответы", callback_data="stop_responses")
kb4.button(text="✖️Закрыть", callback_data='close_feedbacks_settings')
kb4.adjust(1)
kb4 = kb4.as_markup()

kb5 = InlineKeyboardBuilder()
kb5.button(text="📄Подробнее про API", callback_data='about_api')
kb5.button(text="Вернуться назад", callback_data='back_to_settings')
kb5.adjust(1)
kb5 = kb5.as_markup()

kb6 = InlineKeyboardBuilder()
kb6.button(text="Вернуться назад", callback_data='change_api_key')
kb6 = kb6.as_markup()

kb7 = InlineKeyboardBuilder()
kb7.button(text="✅Возобновить ответы на отзывы", callback_data='continue_feedbacks')
kb7 = kb7.as_markup()
