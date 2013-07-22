from bottle import run, get, post, install, JSONPlugin, request
from pymongo import MongoClient
from bson import ObjectId
from json import dumps, JSONEncoder
import time
import datetime
from gamestate_module import Gamestate
from action_getter import get_action
import socket


@get('/games/view/<game_id>')
def view(game_id):
    games = get_games_db()
    game = games.find_one({"_id": ObjectId(game_id)})
    if not game:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    return game


@post('/games/<game_id>/do_action')
def do_action_post(game_id):
    games = get_games_db()
    game = games.find_one({"_id": ObjectId(game_id)})
    if not game:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    gamestate = Gamestate.from_document(game)
    action = get_action(gamestate, request.json)

    available_actions = gamestate.get_actions()
    if not action:
        return invalid_action(available_actions, request.json)

    if not action in available_actions:
        invalid_action(available_actions, str(action))

    gamestate.do_action(action)
    game = gamestate.to_document()
    games.update({"_id": ObjectId(game_id)}, game)
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
