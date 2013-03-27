from bottle import get, run
from pymongo import MongoClient
import time
import datetime


# @get('/games/<game>/move/<move>')
# def move(game, move):
#     client = MongoClient()
#     db = client.unnamed
#     games = db.games
#     pass


@get('/games/new')
def new_game():
    client = MongoClient()
    db = client.unnamed
    games = db.games
    game = {
        "Player1": "Mads",
        "Player1Intelligence": "Human",
        "Player2": "Jonatan",
        "Player2Intelligence": "Human",
        "ActivePlayer": 1,
        "Turn": 1,
        "Actions": 1,
        "ExtraAction": False,
        "Player1Units":
        {
            "D6":
            {
                "Name": "Heavy_Cavalry",
                "AttackCounters": 1,
                "Experience:": 1
            }
        },
        "Player2Units":
        {
            "C7": "Royal_Guard",
            "E7": "Archer"
        },
        "Created": datetime.datetime.utcnow()
    }
    game_id = games.insert(game)
    return {"Status": "OK", "ID": str(game_id), "ServerTime": time.time()}

@get('/hello/<name>')
def hello(name='World'):
    return "Hello ", name, "!"

run(host='localhost', port=8080, debug=True)