import traceback

from aiogram import types
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

from wb_assistance_bot.db import users_db
from wb_assistance_bot.tg_bot import bot
from wb_assistance_bot.tg_bot.keyboards import advertising_kb
from wb_assistance_bot.tg_bot.prepared_text import advertising_text
from wb_assistance_bot.wb.exceptions import UnauthorizedException
from wb_assistance_bot.wb.financial_report import advertising_info, products_info
from wb_assistance_bot.wb.advertising import advertising_companies
from wb_assistance_bot.tg_bot.prepared_text import advertising_text

router = Router()


class Form(StatesGroup):
    getting_api_key = State()
    showing_info = State()


@router.message(Command("advertising"))
async def advertising(message: Message):
    adv_key = await users_db.get_api_advertising(message.from_user.id)
    if (adv_key != "new_user") and (adv_key != "incorrect_api"):
        await Adv_info(message)
    else:
        await message.answer(text=advertising_text.advertising_info,
                             reply_markup=advertising_kb.kb,
                             parse_mode=ParseMode.HTML)


@router.callback_query(lambda c: c.data == "change_advertising_api_key")
async def changing_api_advertise(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text(advertising_text.instruction_api_text,
                                           parse_mode=ParseMode.HTML)
    await callback_query.message.edit_reply_markup(reply_markup=advertising_kb.kb1)
    await state.update_data({'message_id': callback_query.message.message_id})
    await state.set_state(Form.getting_api_key)


@router.callback_query(lambda c: c.data == "back_to_api")
async def changing_api_advertise(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.message.delete()
    await bot.send_message(callback_query.message.chat.id,
                           text="Для работы с разделом предоставьте API-ключ",
                           reply_markup=advertising_kb.kb,
                           parse_mode=ParseMode.HTML)
    await state.clear()


@router.message(Form.getting_api_key)
async def change_key(message: Message, state: FSMContext):
    await users_db.set_api_advertising(message.from_user.id,
                                       message.text)
    state_data = await state.get_data()
    await bot.delete_message(chat_id=message.chat.id, message_id=state_data['message_id'])
    await message.delete()
    await bot.send_message(chat_id=message.chat.id,
                           text="✅ Ключ успешно сохранен")
    await state.clear()
    await Adv_info(message)


async def Adv_info(message: Message):
    try:
        key = await users_db.get_api_advertising(message.from_user.id)
        products = products_info.Products(key).get_products()
        prod_info = {}
        for prod in products["cards"]:
            nmId = prod["nmID"]
            article = prod["vendorCode"]
            title = prod["title"]
            prod_info[nmId] = {
                "article": article,
                "title": title
            }
        advertises = advertising_companies.Advertise(key).get_advertising_cost()
        advs = []
        for advert in advertises["adverts"]:
            if (advert["status"] == 9 or advert["status"] == 11) and (advert["type"] == 8 or advert["type"] == 9):
                advs.append(advert)
        adv_info_getter = advertising_info.AdvertieseInfo(key)
        for adv in advs:
            type = adv["type"]
            status = adv["status"]
            adId_nmId = {}
            for ad in adv["advert_list"]:
                adId = ad["advertId"]
                adv_info = adv_info_getter.get_advertising_information(adId)[0]
                adName = adv_info["name"]
                if "unitedParams" in adv_info.keys():
                    nmId = adv_info["unitedParams"][0]["nms"][0]
                else:
                    try:
                        nmId = adv_info["autoParams"][0]["nms"][0]
                    except:
                        nmId = adv_info["autoParams"]["nms"][0]
                adId_nmId[adId] = [nmId, adName]
            text_to_send = ""
            if type == 8:
                # авто
                text_to_send = advertising_text.auto_text
            else:
                # аукцион
                text_to_send = advertising_text.auction_text
            kb = InlineKeyboardBuilder()
            for adId in adId_nmId.keys():
                card = adId_nmId[adId]
                article = prod_info[card[0]]["article"]
                kb.button(text=f"{article}, {card[1]}", callback_data=str(adId))
            kb.adjust(1)
            kb = kb.as_markup()
            await message.answer(text_to_send, reply_markup=kb, parse_mode=ParseMode.HTML)

    except UnauthorizedException:
        await users_db.set_api_advertising(message.from_user.id, "incorrect_api")
        await message.answer("API-ключ некорректный")
    except Exception as e:
        print(traceback.format_exc())
        if str(e) == "Много запросов":
            await message.answer("WB не успевают предоставлять данные, подождите")
        elif str(e) != "Wb лажает":
            await users_db.set_api_advertising(message.from_user.id, "incorrect_api")
            await message.answer("API-ключ некорректный")
        elif str(e) == "WB лажает":
            await Adv_info(message)


@router.callback_query()
async def catch_all_callbacks(callback: types.CallbackQuery):
    try:
        adId = int(callback.data)
        try:
            key = await users_db.get_api_advertising(callback.from_user.id)
            products = products_info.Products(key).get_products()
            prod_info = {}
            for prod in products["cards"]:
                nmId = prod["nmID"]
                article = prod["vendorCode"]
                title = prod["title"]
                prod_info[nmId] = {
                    "article": article,
                    "title": title
                }
            adv_info_getter = advertising_info.AdvertieseInfo(key)
            adv_info = adv_info_getter.get_advertising_information(adId)[0]
            adName = adv_info["name"]
            adId_nmId = {}
            if "unitedParams" in adv_info.keys():
                nmId = adv_info["unitedParams"][0]["nms"][0]
                searchCPM = adv_info["unitedParams"][0]["searchCPM"]
            else:
                try:
                    nmId = adv_info["autoParams"][0]["nms"][0]
                    searchCPM = adv_info["autoParams"][0]["nmCPM"][0]["cpm"]
                except:
                    nmId = adv_info["autoParams"]["nms"][0]
                    searchCPM = adv_info["autoParams"]["nmCPM"][0]["cpm"]
            adId_nmId[adId] = [nmId, adName]
            for adId in adId_nmId.keys():
                card = adId_nmId[adId]
                article = prod_info[card[0]]["article"]
                title = prod_info[card[0]]["title"]
            status = adv_info["status"]
            type = adv_info["type"]
            text_to_send = ""
            if type == 9:
                fixed_phrases = adv_info["searchPluseState"]
                if fixed_phrases:
                    text_to_send = "Фиксированные фразы активны"
                else:
                    text_to_send = "Фиксированные фразы неактивны"
            text = (f"Информация по кампании {hbold(adName)}\n\n"
                    f"{title}\n\n"
                    f"Артикул: {hbold(article)}\n\n"
                    f"Рекламная ставка: {hbold(searchCPM)}")
            if text_to_send != "":
                text = text + "\n\n" + text_to_send
            await bot.send_message(callback.from_user.id, text=text, parse_mode=ParseMode.HTML)

        except UnauthorizedException:
            await users_db.set_api_advertising(callback.from_user.id, "incorrect_api")
            await callback.answer("API-ключ некорректный")
        except Exception as e:
            print(traceback.format_exc())
            if str(e) == "Много запросов":
                await callback.answer("WB не успевают предоставлять данные, подождите")
            elif str(e) != "Wb лажает":
                await users_db.set_api_advertising(callback.from_user.id, "incorrect_api")
                await callback.answer("API-ключ некорректный")
    except ValueError:
        pass