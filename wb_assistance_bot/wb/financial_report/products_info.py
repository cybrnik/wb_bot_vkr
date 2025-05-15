import json
import time
from time import sleep
import asyncio

import requests
from urllib.parse import urljoin

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class Products:
    url = "https://content-api.wildberries.ru/"

    def __init__(self, key):
        self.key = key

    def __process_response(self, response):
        if response.status_code == 200:
            return response

        if response.status_code == 429:
            raise Exception("Много запросов")

        if response.status_code == 500 or response.status_code == 503 or response.status_code == 403:
            raise Exception("Wb лажает")

        elif response.status_code == 401:
            raise UnauthorizedException()
        else:
            try:
                error_text = response.json()["errorText"]
            except KeyError:
                raise Exception(json.dumps(response.json()))
            raise Exception(error_text)

    def __post_request(self, prefix):
        headers = {
            "Authorization": self.key,
            "Content-Type": 'application/json'
        }
        body = {
            "settings": {
                "cursor": {
                    "limit": 100  # можно изменить в зависимости от твоих нужд
                },
                "filter": {
                    "withPhoto": -1  # это фильтр, чтобы не получать карточки без фото
                }
            }
        }
        response = requests.post(urljoin(self.url, "content/v2/" + prefix), headers=headers, json=body)
        return self.__process_response(response)

    def get_products(self):
        response = self.__post_request(prefix="get/cards/list")
        return response.json()
