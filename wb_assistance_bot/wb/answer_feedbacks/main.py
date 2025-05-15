import os
import json
from wb_assistance_bot.wb.answer_feedbacks.wb_bot import Bot

key = os.getenv("WB_API_KEY")
wb_bot = Bot(key=key)
feedbacks = wb_bot.get_feedbacks()

with open("tmp.json", "w") as f:
    json.dump(feedbacks, f, indent=4)

ids = [feedback["id"] for feedback in feedbacks["data"]["feedbacks"]]
for id in ids:
    code = wb_bot.patch_feedbacks_2(id=id, text="Большое спасибо за отзыв!")
    print(code)
