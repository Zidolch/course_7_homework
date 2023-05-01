import logging

import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse
from todolist.settings import BOT_TOKEN


class TgClient:
    def __init__(self, token: str | None = None):
        self.token = token if token else BOT_TOKEN

    def get_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdates')
        params = {'offset': offset, 'timeout': timeout}

        try:
            response = requests.get(url=url, params=params)
        except Exception as e:
            logging.error('Failed to get updates')
            raise e

        else:
            return GetUpdatesResponse(**response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url('sendMessage')
        data = {'chat_id': chat_id, 'text': text}
        try:
            response = requests.post(url=url, data=data)
        except Exception as e:
            logging.error('Failed to send message')
            raise e
        else:
            return SendMessageResponse(**response.json())
