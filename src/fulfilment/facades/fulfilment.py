import requests


class FulfilmentAPI:
    def __init__(self, login: str, password: str, api_link: str) -> None:
        self.headers = {
            "Login": login,
            "Password": password
        }
        self.api_link = api_link

    def _post_request(self, sub_link: str, data: dict) -> requests.Response:
        return requests.post(url=f"{self.api_link}{sub_link}", headers=self.headers, json=data)

    def create_order(self, data: dict):
        return self._post_request(data=data, sub_link="order")

    def get_order_status(self, data: dict):
        return self._post_request(data=data, sub_link="status")
