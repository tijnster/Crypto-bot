import os
from binance.enums import *
import websocket, json, pprint, talib, numpy
from telegram_client import TelegramClient
from binance_client import BinanceClient

class Cryptobot():

    def __init__(self, capabilities) -> None:
        # initialize binance client
        API_KEY=os.environ.get('API_KEY')
        SECRET_KEY=os.environ.get('SECRET_KEY')
        self.binanceClient = BinanceClient(API_KEY=API_KEY, SECRET_KEY=SECRET_KEY)

        # initialize telegram client
        TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
        TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage?chat_id=84916397&".format(TELEGRAM_TOKEN)
        self.telegramClient = TelegramClient(TELEGRAM_URL)

        # keep track of closing values and positions
        self.closes = []
        self.in_position = False
        self.capabilities = capabilities

    def on_open(ws):
        print("opened connection")

    def on_close(ws):
        print("Closed connection")

    def on_message(self, ws, message):
        print("Message received")

        json_message= json.loads(message)
        pprint.pprint(json_message)

        # retrieving closed price
        candle = json_message['k']
        is_candle_closed = candle['x']
        close = candle['c']

        if is_candle_closed:
            print("Candle closed at {}".format(close))
            self.closes.append(float(close))
            print("Closes")
            print(self.closes)
        
            if len(self.closes) > self.capabilities['RSI_PERIOD']:
                np_closes = numpy.array(self.closes)
                rsi = talib.RSI(np_closes, self.capabilities['RSI_PERIOD'])
                print("All rsi's calculated so far:")
                print(rsi)
                last_rsi = rsi[-1]
                print("The current RSI is: {}".format(last_rsi))

                if last_rsi > self.capabilities['RSI_OVERBOUGHT']:
                    if self.in_position:
                        print("Sell! Sell! Sell!")
                        order = self.binanceClient.order(SIDE_SELL, self.capabilities['TRADE_QUANTITY'], self.capabilities['TRADE_SYMBOL'])
                        if order['succeeded']:
                            message = {'text': 'Congrats! You completed a {} trade for {}. The traded quantity was {} for {}'.format(SIDE_SELL,self.capabilities['TRADE_SYMBOL'], self.capabilities['TRADE_QUANTITY'], order['price'])}
                            self.telegramClient.send_order_to_telegram(message)
                            self.in_position = False
                    else:   
                        print("We don't own any, nothing to do.")
                    

                if last_rsi < self.capabilities['RSI_OVERSOLD']:
                    if self.in_position:
                        print("It is oversold, but you already own it, nothing to do.")
                    else:   
                        print("Buy! Buy! Buy!")
                        order = self.binanceClient.order(SIDE_BUY, self.capabilities['TRADE_QUANTITY'], self.capabilities['TRADE_SYMBOL'])
                        if order['succeeded']:
                            print("Sending message to telegram..")
                            message = {'text': 'Congrats! You completed a {} trade for {}. The traded quantity was {} for {}'.format(SIDE_BUY,self.capabilities['TRADE_SYMBOL'], self.capabilities['TRADE_QUANTITY'], order['price'])}
                            self.telegramClient.send_order_to_telegram(message)
                            self.in_position = True 

    def initialize_socket(self,socket):
        socket=socket
        ws = websocket.WebSocketApp(socket, on_open=self.on_open, on_close=self.on_close, on_message=self.on_message)
        ws.run_forever()
    




