from binance_f import RequestClient
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.model import *
from binance_f.constant.test import *
from binance_f.websocket import *
import json
from flask import Flask

app = Flask(__name__)

# Connect to Binance Futures TestNet
api_key = '0d1e94b104dd54fde98dec9a83f8916b1af3daa0c81c8c754b59ce3d62c8a00a'
secret_key = 'fd6302c060bdf02d8c5e369cc433eb802f6fa09b22317ae1a113f5ff86c40841'
request_client = RequestClient(api_key=api_key, secret_key=secret_key, url=TESTNET_URL)

# Fetch Bitcoin Price using WebSocket
def on_message(ws, message):
    json_message = json.loads(message)
    if 'e' in json_message and json_message['e'] == 'aggTrade' and json_message['s'] == 'BTCUSDT':
        print(f"Current price of BTCUSDT: {json_message['p']}")
        
def on_error(ws, error):
    print(f"Websocket error: {error}")

def on_close(ws):
    print("Websocket closed")

def on_open(ws):
    ws.subscribe_aggregate_trade_event(symbol="btcusdt")

websocket_client = SubscriptionClient()
websocket_client.subscribe_aggregate_trade_event("btcusdt", on_message)

# Post Market Order for $500 at a Leverage of 3x in BTCUSDT Pair
@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        order_response = request_client.post_order(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            ordertype=OrderType.MARKET,
            quantity=10,  # quantity in USD
            positionSide=PositionSide.BOTH,
            newClientOrderId="my_order_id",
            leverage=3
        )
        return {'success': True, 'order_response': order_response}
    except BinanceApiException as e:
        return {'success': False, 'error': e.message}

if __name__ == '__main__':
    app.run(debug=True)
