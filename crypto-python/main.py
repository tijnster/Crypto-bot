from cryptobot import Cryptobot
import json

if __name__ == "__main__":
    with open('capabilities.json', 'r') as f:
        capabilities = json.load(f)

    mybot = Cryptobot(capabilities)
    mybot.initialize_socket("wss://stream.binance.com:9443/ws/vetusdt@kline_15m")
