from aiogram.utils.keyboard import InlineKeyboardBuilder

kb1 = InlineKeyboardBuilder()
kb1.button(text="Все понятно, идем дальше!", callback_data="tax_system")
kb1.adjust(1)
kb1 = kb1.as_markup()

kb2 = InlineKeyboardBuilder()
kb2.button(text="Доходы", callback_data="incomes")
kb2.button(text="Доходы минус расходы", callback_data="incomes_expenses")
kb2.adjust(1)
kb2 = kb2.as_markup()
