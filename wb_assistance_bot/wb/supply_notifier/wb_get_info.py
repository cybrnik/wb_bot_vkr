import json
import requests
from urllib.parse import urljoin

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class Statistics:
    url = "https://statistics-api.wildberries.ru/"

    def __init__(self, key):
        self.key = key

    def __process_response(self, response):
        if response.status_code == 200:
            return response

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

    def get_orders(self, date_from=None):
        params = {}
        if date_from is not None:
            params["dateFrom"] = date_from

        response = self.__get_request(prefix="supplier/orders", params=params)
        return response.json()

    def get_remains(self, date_from=None):
        params = {}
        if date_from is not None:
            params["dateFrom"] = date_from

        response = self.__get_request(prefix="supplier/stocks", params=params)
        return response.json()
