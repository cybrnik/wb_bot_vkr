import threading
import time
import traceback
import asyncio

from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from wb_assistance_bot.tg_bot.bot import bot
from wb_assistance_bot.wb.answer_feedbacks.wb_bot import Bot
from wb_assistance_bot.wb.exceptions import UnauthorizedException
from wb_assistance_bot.db.users import users_db


class Feedbacks:
    def __init__(self, db, every=10):
        self.db = db
        self.every = every

    async def answer_reviews(self):
        users_info = await users_db.get_apis_and_patterns()
        for api, cur_response, pattern1, pattern2, pattern3, pattern4, pattern5, user_id, reg_date, active_responses in users_info:
            if active_responses != 1:
                continue
            if reg_date == None:
                continue
            if api == "incorrect_api" or api == "new_user":
                continue
            wb_bot = Bot(key=api)
            try:
                feedbacks = wb_bot.get_feedbacks()
            except ConnectionError:
                continue
            except UnauthorizedException:
                await bot.send_message(chat_id=user_id,
                                       text=f"🚨 Присланный API-ключ для отзывов не является рабочим\n\n"
                  f"1️⃣ Перейдите в настройки с помощью команды {hbold('/auto_feedback')}\n\n"
                                            f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                            f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                       parse_mode=ParseMode.HTML)
                await users_db.set_api_feedbacks(user_id, "incorrect_api")
                continue
            except UnicodeEncodeError:
                await bot.send_message(chat_id=user_id,
                                       text="🚨 Присланный API-ключ для отзывов не является рабочим\n\n"
                  f"1️⃣ Перейдите в настройки с помощью команды {hbold('/auto_feedback')}\n\n"
                                            f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                            f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                       parse_mode=ParseMode.HTML)
                await users_db.set_api_feedbacks(user_id, "incorrect_api")
                continue
            except Exception as e:
                print(traceback.format_exc())
                if str(e) != "Wb лажает":
                    await bot.send_message(chat_id=user_id,
                                           text="🚨 Присланный API-ключ для отзывов не является рабочим\n\n"
                      f"1️⃣ Перейдите в настройки с помощью команды {hbold('/auto_feedback')}\n\n"
                                                f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                                f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                           parse_mode=ParseMode.HTML)
                    await users_db.set_api_feedbacks(user_id, "incorrect_api")
                continue

            ids = [(feedback["id"], feedback["productValuation"]) for feedback in feedbacks["data"]["feedbacks"]]
            for id, brawl_stars in ids:
                code = 1337
                try:
                    num_responses = await users_db.get_num_responses(user_id)
                    num_responses += 1
                    if brawl_stars == 1:
                        code = wb_bot.patch_feedbacks_2(id=id, text=pattern1)
                    if brawl_stars == 2:
                        code = wb_bot.patch_feedbacks_2(id=id, text=pattern2)
                    if brawl_stars == 3:
                        code = wb_bot.patch_feedbacks_2(id=id, text=pattern3)
                    if brawl_stars == 4:
                        code = wb_bot.patch_feedbacks_2(id=id, text=pattern4)
                    if brawl_stars == 5:
                        code = wb_bot.patch_feedbacks_2(id=id, text=pattern5)
                    await users_db.set_num_responses(user_id=user_id, num_responses=num_responses)

                    # Задержка в 1 секунду после отправки ответа, чтобы не банили)
                    await asyncio.sleep(1)

                except UnauthorizedException:
                    await bot.send_message(
                        chat_id=user_id,
                        text=f"👓 Присланный API-ключ для отзывов работает только на чтение, бот не сможет оставлять отзывы\n\n"
   f"1️⃣ Перейдите в настройки с помощью команды {hbold('/auto_feedback')}\n\n"
                             f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                             f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                        parse_mode=ParseMode.HTML
                    )
                    await users_db.set_api_feedbacks(user_id, "incorrect_api")
                except Exception as e:
                    # если ошибка со стороны сервера, просто подождем
                    if str(e) != "Wb лажает":
                        print(code)
                        print(traceback.format_exc())
                        await users_db.set_api_feedbacks(user_id, "incorrect_api")
                        await bot.send_message(chat_id=user_id,
                                               text="🚨 Присланный API-ключ для отзывов не является рабочим\n\n"
                           f"1️⃣ Перейдите в настройки с помощью команды {hbold('/auto_feedback')}\n\n"
                                                    f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                                    f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                               parse_mode=ParseMode.HTML)
                    else:
                        await asyncio.sleep(30)
                    continue

    async def run(self):
        while self.is_running:
            await self.answer_reviews()
            await asyncio.sleep(self.every)

    async def start_polling(self):
        self.is_running = True
        await self.run()

    async def stop_polling(self):
        self.is_running = False
