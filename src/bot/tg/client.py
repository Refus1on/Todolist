import requests
from requests import Response

from bot.tg.models import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response: Response = requests.get(url=self.get_url("getUpdates"), params={"offset": offset, "timeout": timeout})
        data = response.json()
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        response: Response = requests.get(url=self.get_url("sendMessage"), params={
            "chat_id": chat_id,
            "text": text
        })
        data = response.json()
        return SendMessageResponse(**data)
