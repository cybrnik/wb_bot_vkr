import glob
import io
import os
import traceback
import asyncio
import pandas as pd
import dateutil.parser

from datetime import datetime, timedelta, time
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile, BufferedInputFile
from aiogram.utils.markdown import hbold
from wb_assistance_bot.wb.exceptions import UnauthorizedException
from wb_assistance_bot.db.users import users_db
from wb_assistance_bot.tg_bot.bot import bot
from wb_assistance_bot.wb.supply_notifier.wb_get_info import Statistics

current_date = datetime.now().date()
last_day = current_date - timedelta(days=1)
last_day = last_day.strftime("%Y-%m-%d")
first_day = current_date - timedelta(days=7)
first_day = first_day.strftime("%Y-%m-%d")

Regions = {
    'Центральный федеральный округ': {'Коледино', 'Электросталь', 'Котовск', 'Рязань', 'Рязань (Тюшевское)',
                                      'Волгоград', 'Подольск 4', 'Тула'},
    'Северо-Западный федеральный округ': {'Санкт-Петербург', 'Уткина Заводь'},
    'Приволжский федеральный округ': {'Казань'},
    'Уральский федеральный округ': {'Екатеринбург - Перспективный 12', 'Екатеринбург - Испытателей 14г'},
    'Южный федеральный округ': {'Краснодар', 'Невинномысск'},
    'Сибирский федеральный округ': {'Новосибирск'},
    'Дальневосточный федеральный округ': {'Хабаровск'}
}

Regions_sales_percent = {
    'Центральный федеральный округ': 30,
    'Северо-Западный федеральный округ': 6.9,
    'Уральский федеральный округ': 9.9,
    'Дальневосточный федеральный округ': 15.3,
    'Приволжский федеральный округ': 16,
    'Южный федеральный округ': 13.1
}


def normer_sales_percent_by_region(r1='округ', r2='округ', r3='округ', r4='округ', r5='округ', r6='округ', r7='округ'):
    regions = [r1, r2, r3, r4, r5, r6, r7]
    passed_regions = [r for r in regions if r != 'округ']
    passed_regions_percent = []
    for reg in passed_regions:
        passed_regions_percent.append(Regions_sales_percent[reg])
    total = sum(passed_regions_percent)
    normalized = [(val / total) * 100 for val in passed_regions_percent]
    ret = []
    for i in range(len(passed_regions)):
        ret.append([passed_regions[i], normalized[i]])
    return ret


def normer_sales_percent(arr):
    total = sum(arr)
    normalized = [(val / total) * 100 for val in arr]
    return normalized


class Checking_supplies:
    def __init__(self, db, every=200):
        self.db = db
        self.every = every

    async def check_orders_and_quantities(self):
        # также очистим папку с отчетами
        folder_path = 'reports'
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except Exception as e:
                    print(f'Ошибка при удалении {file_path}: {e}')
        users_info = await users_db.get_all_statistics_api()
        for api, user_id in users_info:
            if api == "incorrect_api" or api == "new_user":
                continue
            wb_bot = Statistics(key=api)
            try:
                orders = wb_bot.get_orders(date_from=first_day)
                remains = wb_bot.get_remains(date_from=first_day)
            except UnauthorizedException:
                await bot.send_message(chat_id=user_id,
                                       text=f"🚨 Присланный API-ключ для поставок не является рабочим\n\n"
                                            f"1️⃣ Перейдите в настройки с помощью комманды {hbold('/supply_notifier')}\n\n"
                                            f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                            f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                       parse_mode=ParseMode.HTML)
                await users_db.set_statistics_api(user_id, "incorrect_api")
                continue
            except UnicodeEncodeError:
                await bot.send_message(chat_id=user_id,
                                       text="🚨 Присланный API-ключ для поставок не является рабочим\n\n"
                                            f"1️⃣ Перейдите в настройки с помощью комманды {hbold('/supply_notifier')}\n\n"
                                            f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                            f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                       parse_mode=ParseMode.HTML)
                await users_db.set_statistics_api(user_id, "incorrect_api")
                continue
            except Exception as e:
                print(traceback.format_exc())
                if str(e) != "Wb лажает":
                    await bot.send_message(chat_id=user_id,
                                           text="🚨 Присланный API-ключ для отзывов не является рабочим\n\n"
                                                f"1️⃣ Перейдите в настройки с помощью комманды {hbold('/auto_feedback')}\n\n"
                                                f"2️⃣ Нажмите на кнопку [✍️Сменить API ключ]\n\n"
                                                f"3️⃣ Отправьте рабочий ключ, создав его по инструкции",
                                           parse_mode=ParseMode.HTML)
                    await users_db.set_api_feedbacks(user_id, "incorrect_api")
                continue

            region_sales = {}
            article_sales = {}

            for order in orders:
                order_date = order["date"]
                order_date = dateutil.parser.parse(order_date).date()
                if (not order["isCancel"]) and (order_date < current_date):
                    article = order["supplierArticle"]
                    region = order["oblastOkrugName"]
                    if article in article_sales:
                        article_sales[article] += 1
                    else:
                        article_sales[article] = 1
                    if region in region_sales:
                        if article in region_sales[region]:
                            region_sales[region][article] += 1
                        else:
                            region_sales[region][article] = 1
                    else:
                        region_sales[region] = {}
                        region_sales[region][article] = 1

            region_quantities = {}
            article_remains = {}

            for remain in remains:
                article = remain["supplierArticle"]
                warehouse = remain["warehouseName"]
                quantity = remain["quantity"]
                if quantity > 0:
                    region = ""
                    for key in Regions:
                        if warehouse in Regions[key]:
                            region = key
                    if region == "":
                        print(quantity)
                        print("Не завел такой регион под склад:" + warehouse)
                        continue
                    if quantity > 0:
                        if article in article_remains:
                            article_remains[article] += quantity
                        else:
                            article_remains[article] = quantity
                        if region in region_quantities:
                            if article in region_quantities[region]:
                                region_quantities[region][article] += quantity
                            else:
                                region_quantities[region][article] = quantity
                        else:
                            region_quantities[region] = {}
                            region_quantities[region][article] = quantity

            info_to_send_user1 = ("⬇️ Ниже отображается информация следующего формата\n\n"
                                  f"{hbold("👜Артикул товара + ⏰число дней до выхода из наличия")}\n\n")

            flag_to_send1 = False
            num = 1

            days_to_notify = 15

            for article in article_sales.keys():
                mean_sales = article_sales[article] // 7
                mean_sales += mean_sales * 0.1  # средние продажи увеличиваем на 10% в силу роста
                mean_sales = int(mean_sales)
                if mean_sales != 0:
                    if article in article_remains:
                        if article_remains[article] / mean_sales <= days_to_notify:
                            days_left = article_remains[article] / mean_sales
                            if int(days_left) < 1:
                                days_left = 1
                            else:
                                days_left = int(days_left)
                            flag_to_send1 = True
                            info_to_send_user1 += hbold(str(num)) + ") " + hbold(article) + "  -  " + hbold(
                                days_left) + "\n\n"
                            num += 1

            days_to_sale = 20

            info_to_send_user2 = ("⬇️ Ниже отображается информация следующего формата\n\n"
                                  f"{hbold("👜 Артикул товара + 🏠 Регион + ⏰ число дней до выхода из наличия")}\n\n")

            num = 1

            articles_regions_percent = {}

            for region in region_quantities.keys():
                for article in region_quantities[region]:
                    if region_quantities[region][article] <= 1:
                        continue
                    if article in articles_regions_percent:
                        articles_regions_percent[article].append([Regions_sales_percent[region], region])
                    else:
                        articles_regions_percent[article] = [[Regions_sales_percent[region], region]]

            for article in articles_regions_percent:
                total = 0
                for reg in articles_regions_percent[article]:
                    total += reg[0]
                for reg in articles_regions_percent[article]:
                    reg[0] = reg[0] / total * 100

            df = pd.DataFrame(columns=['Артикул товара', 'Регион', 'Остаток на складе', 'Количество для отгрузки'])

            for article in articles_regions_percent:
                mean_sales = article_sales[article] // 7
                mean_sales += mean_sales * 0.1
                if mean_sales == 0:
                    continue
                for reg in articles_regions_percent[article]:
                    region = reg[1]
                    percent = reg[0]
                    days_left = region_quantities[region][article] / (mean_sales * percent / 100)
                    if days_left <= days_to_notify:
                        if int(days_left) < 1:
                            days_left = 1
                        else:
                            days_left = int(days_left)
                        to_load = int(mean_sales * percent / 100 * days_to_sale)
                        first_word = region.split()[0]
                        df.loc[len(df)] = [article, first_word, region_quantities[region][article],
                                           to_load]
                        info_to_send_user2 += hbold(str(num)) + ") " + hbold(
                            article) + "  -  " + hbold(first_word) + "  -  " + hbold(
                            days_left) + "\n\n"
                        num += 1

            if flag_to_send1:
                await bot.send_message(chat_id=user_id,
                                       text=info_to_send_user1,
                                       parse_mode=ParseMode.HTML)

            await bot.send_message(chat_id=user_id,
                                   text=info_to_send_user2,
                                   parse_mode=ParseMode.HTML)

            # df.to_excel(f"table_{user_id}.xlsx", index=False)
            # file = FSInputFile(f"table_{user_id}.xlsx")
            buffer = io.BytesIO()
            df.to_excel(buffer, index=False)
            buffer.seek(0)
            file = BufferedInputFile(buffer.read(), filename="table.xlsx")
            await bot.send_document(chat_id=user_id, document=file)

    async def run(self):
        while self.is_running:
            await self.check_orders_and_quantities()
            await asyncio.sleep(self.every)

    async def wait_until_21(self):
        now = datetime.now()
        target_time = datetime.combine(now.date(), time(21, 0))
        if now >= target_time:
            target_time += timedelta(days=1)
        wait_seconds = (target_time - now).total_seconds()
        await asyncio.sleep(wait_seconds)

    async def start_polling(self):
        await self.wait_until_21()
        self.is_running = True
        await self.run()

    async def stop_polling(self):
        self.is_running = False
