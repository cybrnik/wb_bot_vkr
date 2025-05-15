import json
import requests
from urllib.parse import urljoin

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class Report:
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
        response = requests.get(urljoin(self.url, "api/v5/" + prefix), headers=headers, params=params)
        return self.__process_response(response)

    def get_report(self, date_from=None, date_to=None):
        params = {}
        if date_from is not None:
            params["dateFrom"] = date_from
        if date_to is not None:
            params["dateTo"] = date_to
        response = self.__get_request(prefix="supplier/reportDetailByPeriod", params=params)
        return response.json()
