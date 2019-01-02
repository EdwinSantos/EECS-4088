#!/usr/bin/python3
try:
    from eventlet import monkey_patch
    monkey_patch()
    print("Running Eventlet Server")
except ModuleNotFoundError:
    try:
        from gevent import monkey
        monkey.patch_all()
        print("Running Gevent Server")
    except ModuleNotFoundError:
        print("Running Flask Server")

from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, emit
from threading import Thread
import json

from gameList import GameList

# initialize Flask

app = Flask(__name__)
socketio = SocketIO(app)
ROOMS = {} # dict to track active rooms

users = {}
game = None
game_thread = None

# This is a catch-all route, this allow for react to do client-side
# routing and stoping flasks routing
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def index(path):
    return render_template('index.html')

@socketio.on('joinServer')
def join_server(data):
    "Create a game lobby"
    users[data["socketId"]] = data["username"] + " #" + data["socketId"][:4]
    print(users.get(data["socketId"])  + " has logged in")   
    emit('games', {'games': GameList.list_games()})
    emit('username', {'username': users[data["socketId"]]})
    join_room(users[data["socketId"]])  

@socketio.on('createGame')
def create_game(data):
    # emit('gameStarted', 'Double07', broadcast=True)
    # emit('gameOver', broadcast=True)
    global game
    print(users)
    if game is None or not game.is_active():
        game = GameList.select_game(data, users.values())
        emit('gameStarted', game.__name__, broadcast=True)
        global game_thread
        if game_thread is None or not game_thread.isAlive():
            game_thread = Thread(target=game.run_game, args=[socketio])
            game_thread.start()

# def runGame():
#     while game.is_active():
#         emit('state', game.get_state())
#         for i in range(game.get_timer(), 0, -1):
#             print(i)
#             socketio.sleep(1)
#         if game.get_timer():
#             emit('timerExpired', "")
#             print("Waiting for inputs")
#             socketio.sleep(5)
#             print("Times up")
#         game.end_round()
#         game.display()
#     else:
#         emit('gameOver', "")

# @socketio.on('endOfRound')
# def action(data):
#     print(users[request.sid], data)
#     if game.action(data):
#         game.end_round()

# def background():
#     i = 0
#     while True:
#         print(i)
#         i += 1
#         socketio.sleep(1)
        # emit('poll', broadcast=True)

# @socketio.on('pollResponse')
# def polling():
#     print("a")

# ----------------- Chat ------------------

chatLog = []

@socketio.on('sendToServer')
def send_to_server(data):
    if data["type"] == "chat":
        chatLog.append(data)
        # broadcast allows for all connected socket to receive the message
        emit('chatLogFromServer', chatLog, broadcast=True)
    elif data["type"] == "chatLog":
        emit('chatLogFromServer', chatLog, broadcast=True)
    elif data["type"] == "retrieveUsers":
        emit('userList', users, broadcast=True)
    elif data["type"] == "retrieveUsername":
        emit('username', users[request.sid])


'''
There should be no game logic inside the server
'''
# ----------------- 007 GAME ------------------

# players stores username, socket id, lives, action points of all players
# players = {}
# actions stores each users actions in the current round
# actions = []
# function endOfRound cycles through the actions list and applies those actions
# to players, updating players list

# broadcast is set to true so that when a user joins a game, it tells all other users
# in the game an updated opponents list

# @socketio.on('initializePlayers')
# def initializePlayers():
#     # reset array on load
#     players = []
#     for user in users:
#         players.append({
#             "username": users[user],
#             "socketId": user,
#             "hp": 3,
#             "ap": 1
#         })
#     emit("allPlayers", players, broadcast=True) 

# @socketio.on('endOfRound')
# def endOfRound(data):
#     print(data)

# ---------------- HOT POTATO GAME ------------------

# When the client disconnects from the socket
@socketio.on('disconnect')
def dc():
    del users[request.sid]
    # let every user know when a user disconnects
    emit("userDisconnected", request.sid, broadcast=True)
    print("dc " + request.sid)

@socketio.on('connect')
def con():
    print("con " + request.sid) 
#     gm = game.Start(socketio)


if __name__ == '__main__':
    # game_thread(target=background).start()
    socketio.run(app, host="0.0.0.0")
    # wsgi.server(eventlet.listen(('0.0.0.0', 5000)), app)
