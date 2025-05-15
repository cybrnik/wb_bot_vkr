import json
import requests
from urllib.parse import urljoin

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class AdvertieseInfo:
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

    def __post_request(self, prefix, data):
        headers = {
            "Authorization": self.key,
            "Content-Type": 'application/json'
        }
        response = requests.post(urljoin(self.url, "adv/v1/" + prefix), headers=headers, json=data)
        return self.__process_response(response)

    def get_advertising_information(self, id=None):
        if id is None:
            raise ValueError("Campaign IDs must be provided")
        if not isinstance(id, list):
            id = [id]
        if not all(isinstance(i, int) for i in id):
            raise TypeError("Expected list of integers in 'id'")
        response = self.__post_request(prefix="promotion/adverts", data=id)
        return response.json()
