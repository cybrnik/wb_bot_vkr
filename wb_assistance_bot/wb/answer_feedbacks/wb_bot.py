import os
import json
import requests

from wb_assistance_bot.wb.exceptions import UnauthorizedException


class Bot:
    def __init__(self, key):
        self.key = key
        self.url = "https://feedbacks-api.wildberries.ru"

    def __process_response(self, response):
        if response.status_code == 200 or response.status_code == 204:
            return response

        if response.status_code == 500 or response.status_code == 503 or response.status_code == 403:
            raise Exception("Wb лажает")

        elif response.status_code == 401:
            raise UnauthorizedException("Unauthorized request - Invalid API key or session.")

        try:
            response_data = response.json()
            error_text = response_data.get("errorText", "Unknown error")
        except json.JSONDecodeError:
            raise Exception(f"Failed to decode JSON response: {response.text}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
        if error_text != "Unknown error":
            raise Exception(error_text)
        raise Exception(f"Unexpected response structure: {response.text}")

    def __get_request(self, prefix, params={}):
        headers = {"Authorization": self.key}
        url_get_request = f"{self.url}/api/v1/{prefix}"
        try:
            response = requests.get(url_get_request, headers=headers, params=params, timeout=10)
            return self.__process_response(response)
        except ConnectionError:
            raise Exception("Connection error: Unable to reach the server.")
        #response = requests.get(url_get_request, headers=headers, params=params)
        #return self.__process_response(response)

    def __patch_request(self, prefix, data={}):
        headers = {"Authorization": self.key}
        url_patch_request = f"{self.url}/api/v1/{prefix}"
        response = requests.post(url_patch_request, headers=headers, json=data)
        return self.__process_response(response)

    def count_unanswered(self):
        response = self.__get_request(prefix="feedbacks/count-unanswered")
        return response.json()

    def get_feedbacks(self, is_answered=False, nm_id=None, take=5000, skip=0, order=None, date_from=None, date_to=None):
        params = {
            "isAnswered": is_answered,
            "take": take,
            "skip": skip
        }
        if nm_id is not None:
            params["nmId"] = nm_id
        if order is not None:
            params["order"] = order
        if date_from is not None:
            params["dateFrom"] = date_from
        if date_to is not None:
            params["dateTo"] = date_to

        response = self.__get_request(prefix="feedbacks", params=params)
        return response.json()

    def patch_feedbacks_2(self, id, text):
        data = {
            "id": id,
            "text": text
        }

        response = self.__patch_request(prefix="feedbacks/answer", data=data)
        return response.status_code
