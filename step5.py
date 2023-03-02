from binance_f import RequestClient
from binance_f.exception.binanceapiexception import BinanceApiException
from binance_f.model import *
from binance_f.constant.test import *
import json
from flask import Flask

app = Flask(__name__)

# Connect to Binance Futures TestNet
api_key = '0d1e94b104dd54fde98dec9a83f8916b1af3daa0c81c8c754b59ce3d62c8a00a'
secret_key = 'fd6302c060bdf02d8c5e369cc433eb802f6fa09b22317ae1a113f5ff86c40841'
request_client = RequestClient(api_key=api_key, secret_key=secret_key, url=TESTNET_URL)

# Post Limit Order in BTCUSDT Pair at 0.2% MarkUp of Purchase Price
@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        # Get the current price of BTCUSDT
        ticker_price = request_client.get_symbol_ticker(symbol="BTCUSDT").price

        # Calculate the purchase price with a 0.2% markup
        purchase_price = float(ticker_price) * 1.002

        # Place the limit order
        order_response = request_client.post_order(
            symbol="BTCUSDT",
            side=OrderSide.BUY,
            ordertype=OrderType.LIMIT,
            price=purchase_price,
            quantity=0.001,  # quantity in BTC
            positionSide=PositionSide.BOTH,
            newClientOrderId="my_order_id",
            timeInForce=TimeInForce.GTC
        )
        return {'success': True, 'order_response': order_response}
    except BinanceApiException as e:
        return {'success': False, 'error': e.message}

if __name__ == '__main__':
    app.run(debug=True)
