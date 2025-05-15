from aiogram.utils.keyboard import InlineKeyboardBuilder

kb = InlineKeyboardBuilder()
#kb.button(text="⚙️Настройки автоответов на отзывы", callback_data='feedbacks_settings')
kb.button(text="📱Связь с разработчиками", url="https://t.me/wb_assist_support")
kb.adjust(1)
kb = kb.as_markup()

kb1 = InlineKeyboardBuilder()
kb1.button(text="📱Связь с разработчиками", url="https://t.me/wb_assist_support")
kb1.adjust(1)
kb1 = kb1.as_markup()

kb2 = InlineKeyboardBuilder()
kb2.button(text="✅Возобновить ответы на отзывы", callback_data='continue_feedbacks')
kb2 = kb2.as_markup()
