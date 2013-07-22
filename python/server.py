from bottle import get, run
from pymongo import MongoClient
import time
import datetime
import gamestate_module
from action import Action


@get('/games/<game_id>/do_action/<action_json>')
def do_action(game_id, action_json):
    client = MongoClient()
    database = client.unnamed
    games = database.games

    game = games.find({"_id": game_id})
    if not game:
        return {"Status": "Error", "Message": "Could not find game with id " + game}

    print action_json
    gamestate = gamestate_module.load_json(game)
    action = Action((1, 1), (1, 2), None, False, False, False)
    gamestate.do_action(action)
    game = gamestate.to_json()
    games.update({"_id", game})
    return {"Status": "OK", "Message": "Action recorded"}


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




class CustomJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
        if isinstance(obj, ObjectId):
            return str(obj)
        return JSONEncoder.default(self, obj)

host_address = "10.224.105.151"
if socket.gethostname() == "MD-rMBP.local":
    host_address = "localhost"

install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=CustomJsonEncoder)))
run(host=host_address, port=8080, debug=True)
