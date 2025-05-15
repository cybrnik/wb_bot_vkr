from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = InlineKeyboardBuilder()
kb.button(text="✍️Сменить API ключ", callback_data='change_api_statistics_key')
kb.button(text="✖️Закрыть", callback_data='close_supply_notifier')
kb.adjust(1)
kb = kb.as_markup()

kb1 = InlineKeyboardBuilder()
kb1.button(text="📄Подробнее про API", callback_data='about_api_supplies')
kb1.button(text="Вернуться назад", callback_data='back_to_settings_supplies')
kb1.adjust(1)
kb1 = kb1.as_markup()

kb2 = InlineKeyboardBuilder()
kb2.button(text="Вернуться назад", callback_data='back_to_api_instruction')
kb2.adjust(1)
kb2 = kb2.as_markup()
