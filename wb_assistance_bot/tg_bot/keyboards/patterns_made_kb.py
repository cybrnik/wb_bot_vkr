from aiogram.utils.keyboard import InlineKeyboardBuilder

kb1 = InlineKeyboardBuilder()
kb1.button(text="⭐️", callback_data="1")
kb1.button(text="⭐⭐️️", callback_data="2")
kb1.button(text="⭐️⭐️⭐️", callback_data="3")
kb1.button(text="⭐️⭐️⭐️⭐️", callback_data="4")
kb1.button(text="⭐️⭐️⭐️⭐️⭐️", callback_data="5")
kb1.button(text="Все отлично, ничего менять не будем", callback_data="patterns_done")
kb1.adjust(1)
kb1 = kb1.as_markup()

kb2 = InlineKeyboardBuilder()
kb2.button(text="Вернуться назад", callback_data="back_to_patterns")
kb2 = kb2.as_markup()

kb3 = InlineKeyboardBuilder()
kb3.button(text="📄Подробнее про API", callback_data='about_api_start')
kb3 = kb3.as_markup()

kb4 = InlineKeyboardBuilder()
kb4.button(text="Вернуться назад", callback_data='back_to_instruction_api')
kb4 = kb4.as_markup()
