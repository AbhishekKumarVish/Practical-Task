import websocket
import json
from flask import Flask, jsonify,render_template
app=Flask(__name__)



@app.route('/')
def home():
    return render_template('home.html',price=price)
def on_message(ws, message):
    global price
    data=json.loads(message)

    price = float(data['c'])

if __name__=="__main__":
    price = None
    ws = websocket.WebSocketApp('wss://stream.binancefuture.com/ws',on_message=on_message)

    ws.run_forever()