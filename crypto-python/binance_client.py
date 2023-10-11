from binance import Client
from binance.enums import *

class BinanceClient():

    client = None
    
    def __init__(self, API_KEY, SECRET_KEY):
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = Client(API_KEY, SECRET_KEY)

    def order(self,side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
        order = {'succeeded': False, 'price': None}
        try:
            print("Sending order")
            response = self.client.create_order(symbol=symbol,side=side,type=order_type,quantity=quantity)
            order['succeeded'] = True

            order['price'] = response['fills'][0]['price']
            print(response)
        except Exception as e:
            print(e)

        return order
