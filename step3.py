from flask import Flask,jsonify,request
import hmac
import hashlib

app=Flask(__name__)

@app.route('/')
def welcome():
    wel="App is runnning"
    return wel

API_KEY = '0d1e94b104dd54fde98dec9a83f8916b1af3daa0c81c8c754b59ce3d62c8a00a'
SECRET_KEY = 'fd6302c060bdf02d8c5e369cc433eb802f6fa09b22317ae1a113f5ff86c40841'
BASE_URL = 'https://testnet.binancefuture.com'

def get_balance():
    timestamp = request.get(BASE_URL + '/fapi/v2/time').json()['servertime']

    signature = hmac.new(SECRET_KEY.encode('utf-8'), f'timestamp={timestamp}'.encode('utf-8'),hashlib.sha256.hexdigest())
    

    headers = {'X-MBX-APIKEY':API_KEY}

    payload = {
        'timestamp':timestamp,
        'signature':signature

    }
    response = request.get(BASE_URL + '/fapi.v2.account',headers=headers, params=payload)

    data = response.json()

    for asset in data['assets']:
        if asset['asset'] == 'USDT':
            return float(asset['walletBalance'])
    return None

@app.route('/balance',methods=['GET'])
def get_balance_route():
    balance = get_balance()
    if balance is not None:
        return jsonify({'balance':balance})
    else:
        return jsonify({'error':'USDT balnce not found'})
    
if __name__=="__main__":
    app.run(debug=True)

