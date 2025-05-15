from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = InlineKeyboardBuilder()
kb.button(text="✏️Рассчитать без API", callback_data='finance_no_api')
kb.button(text="🚀Рассчитать с API", callback_data='finance_with_api')
kb.button(text="🔢Указать себестоимости товаров", callback_data='products_cost')
kb.button(text="✍️Сменить API ключ", callback_data='change_finance_api_key')
kb.button(text="✖️Закрыть", callback_data='close_financial_settings')
kb.adjust(1)
kb = kb.as_markup()

kb1 = InlineKeyboardBuilder()
kb1.button(text="📄Подробнее про API", callback_data='about_api_finance')
kb1.button(text="Вернуться назад", callback_data='back_to_finance_menu')
kb1.adjust(1)
kb1 = kb1.as_markup()

kb2 = InlineKeyboardBuilder()
kb2.button(text="Вернуться назад", callback_data='back_to_api_finance')
kb2.adjust(1)
kb2 = kb2.as_markup()

kb3 = InlineKeyboardBuilder()
kb3.button(text="Вернуться назад", callback_data='back_to_finance_menu')
kb3.adjust(1)
kb3 = kb3.as_markup()