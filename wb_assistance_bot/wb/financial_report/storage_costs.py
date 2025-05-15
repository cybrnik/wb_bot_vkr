import json
import time
from time import sleep
import asyncio

import requests
from urllib.parse import urljoin

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class Storage:
    url = "https://seller-analytics-api.wildberries.ru/"

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

    def __get_request(self, prefix, params={}):
        headers = {"Authorization": self.key}
        response = requests.get(urljoin(self.url, "api/v1/" + prefix), headers=headers, params=params)
        return self.__process_response(response)

    def get_storage_cost(self, date_from=None, date_to=None):
        params = {}
        if date_from is not None:
            params["dateFrom"] = date_from
        if date_to is not None:
            params["dateTo"] = date_to
        response = self.__get_request(prefix="paid_storage", params=params)
        response = response.json()
        taskID = response['data']['taskId']
        while True:
            response = self.__get_request(prefix=f"paid_storage/tasks/{taskID}/status", params=params)
            if response.json()['data']['status'] == "done":
                break
            elif response.json()['data']['status'] == "canceled" or response.json()['data']['status'] == "purged":
                time.sleep(60)
                response = self.__get_request(prefix="paid_storage", params=params)
                response = response.json()
                taskID = response['data']['taskId']
            time.sleep(5)
        response = self.__get_request(prefix=f"paid_storage/tasks/{taskID}/download", params=params)
        return response.json()
