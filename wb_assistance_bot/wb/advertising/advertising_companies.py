import json
import requests
from urllib.parse import urljoin

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class Advertise:
    url = "https://advert-api.wildberries.ru/"

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
        response = requests.get(urljoin(self.url, "adv/v1/" + prefix), headers=headers, params=params)
        return self.__process_response(response)

    def get_advertising_cost(self):
        params = {}
        response = self.__get_request(prefix="promotion/count", params=params)
        return response.json()
