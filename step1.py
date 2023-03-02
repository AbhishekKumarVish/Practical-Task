from flask import Flask, request,render_template
from flask_socketio import SocketIO,send

app=Flask(__name__)
app.config['SECRET_KEY'] = 'fd6302c060bdf02d8c5e369cc433eb802f6fa09b22317ae1a113f5ff86c40841'
socketio = SocketIO(app)

@app.route('/websocket')
def websocket():
    return render_template('web.html')

@socketio.on('message')
def handle_message(message):
    print('received message:'+message)
    send(message, broadcast=True)

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    return {'status':'success'}

if __name__=="__main__":
    socketio.run(app,debug=True)