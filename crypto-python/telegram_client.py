import requests

class TelegramClient():

    def __init__(self, TELEGRAM_URL):
        self.TELEGRAM_URL = TELEGRAM_URL
    
    def send_order_to_telegram(self,message: str):
        response = requests.get(self.TELEGRAM_URL, params=message)
        print("response is: " + response.json())
    