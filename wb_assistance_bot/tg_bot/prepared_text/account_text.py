from aiogram.utils.markdown import hbold

ai_lk_text = f"👤 {hbold('Личный кабинет')}\n" + """
Бот уже ответил на столько отзывов: {}

Сейчас бот {} на отзывы
"""


def get_ai_lk_text(text):
    return ai_lk_text.format(hbold(text), hbold("сам генерирует ответы"))


no_ai_lk_text = f"👤{hbold('Личный кабинет')}\n" + """
Бот уже ответил на столько отзывов: {}

Сейчас бот отвечает {} на отзывы
"""


def get_no_ai_lk_text(text):
    return no_ai_lk_text.format(hbold(text), hbold("шаблонами"))


not_making_responses_text = f"👤 {hbold('Личный кабинет')}\n" + """
Бот уже ответил на столько отзывов: {}

Сейчас бот не отвечает на отзывы
"""


def not_making_responses(text):
    return not_making_responses_text.format(hbold(text))
