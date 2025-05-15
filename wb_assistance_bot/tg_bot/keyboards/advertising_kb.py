from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = InlineKeyboardBuilder()
kb.button(text="✍️Сменить API ключ", callback_data="change_advertising_api_key")
kb.adjust(1)
kb = kb.as_markup()

kb1 = InlineKeyboardBuilder()
kb1.button(text="Вернуться назад", callback_data='back_to_api')
kb1.adjust(1)
kb1 = kb1.as_markup()