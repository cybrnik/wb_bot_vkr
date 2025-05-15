import asyncio
import logging
from aiogram import Dispatcher
from wb_assistance_bot.tg_bot.handlers import feedbacks_settings, account, start_handler, supply_notifier, financial_report, advertising
from db import users_db
from tg_bot import bot
from wb.answer_feedbacks.feedbacks import Feedbacks
from wb_assistance_bot.wb.supply_notifier.checking_orders import Checking_supplies

logging.basicConfig(level=logging.INFO)

wb_feedbacks = Feedbacks(users_db, 10)
wb_supply_notifier = Checking_supplies(users_db, 86400)


async def start(bot):
    _ = asyncio.create_task(wb_feedbacks.start_polling())
    _ = asyncio.create_task(wb_supply_notifier.start_polling())


async def shutdown(bot):
    await wb_feedbacks.stop_polling()
    await wb_supply_notifier.stop_polling()
    await users_db.close()


async def main():
    dp = Dispatcher()
    dp.startup.register(start)
    dp.shutdown.register(shutdown)
    dp.include_routers(
        start_handler.router,
        feedbacks_settings.router,
        account.router,
        supply_notifier.router,
        financial_report.router,
        advertising.router
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
