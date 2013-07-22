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


def invalid_action(available_actions, requested_action):
    return {
        "Status": "Error",
        "Message": "Invalid action",
        "Action": requested_action,
        "Available actions": ", ".join(str(action) for action in available_actions)}


@get('/games/new')
def new_game():
    games = get_games_db()
    game = {
        "player1": "Mads",
        "player1_intelligence": "Human",
        "player2": "Jonatan",
        "player2_intelligence": "Human",
        "active_player": 1,
        "turn": 1,
        "actions_remaining": 1,
        "extra_action": False,
        "player1_units":
        {
            "D6":
            {
                "name": "Heavy Cavalry",
                "attack_counters": 1,
                "experience:": 1
            }
        },
        "player2_units":
        {
            "C7": "Royal Guard",
            "E7": "Archer"
        },
        "created_at": datetime.datetime.utcnow()
    }
    game_id = games.insert(game)
    return {"Status": "OK", "ID": str(game_id), "ServerTime": time.time()}


def get_games_db():
    client = MongoClient()
    database = client.unnamed
    return database.games


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
