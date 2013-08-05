from bottle import run, get, post, install, JSONPlugin, request
from pymongo import MongoClient
from bson import ObjectId
from json import dumps
import time
from gamestate import Gamestate
from action_getter import get_action
import socket
from player import Player
import setup
from common import CustomJsonEncoder


@get('/games/view/<game_id>')
def view(game_id):
    games = get_games_db()
    game = games.find_one({"_id": ObjectId(game_id)})
    if not game:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    gamestate = get_current_gamestate(game)

    return gamestate.to_document()


@get("/actions/view/<game_id>")
def view_actions(game_id):
    actions = get_actions_db()
    action_documents = list(actions.find({"game": ObjectId(game_id)}))
    actions_document = dict()
    if action_documents.__len__() > 0:
        actions_document["last_action"] = action_documents[-1]["action_number"]
        actions_document["last_updated_at"] = action_documents[-1]["created_at"]

    for action in action_documents:
        actions_document[action["action_number"]] = action

    return actions_document


@post('/games/<game_id>/do_action')
def do_action_post(game_id):
    games = get_games_db()
    game = games.find_one({"_id": ObjectId(game_id)})
    if not game:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    actions = list(get_actions_db().find({"game": ObjectId(game_id)}).sort("action_number"))

    gamestate = get_current_gamestate(game, actions)

    action_document = request.json

    entirebody = request.body.getvalue()
    print "received: " + entirebody

    action = get_action(gamestate, action_document)

    available_actions = gamestate.get_actions()
    if not action:
        return invalid_action(available_actions, request.json)

    if not action in available_actions:
        return invalid_action(available_actions, str(action))

    action_number = action_document["action_number"]
    expected_action_number = 1
    if len(actions):
        expected_action_number += actions[-1]["action_number"]
    if action_number != expected_action_number:
        return {"Status": "Error", "Message": "The next action must be numbered " + str(expected_action_number)}

    gamestate.do_action(action)
    gamestate.shift_turn_if_done()
    actions = get_actions_db()
    action_document["game"] = ObjectId(game_id)
    action_document["outcome"] = action.outcome == "Success"
    actions.insert(action_document)

    return {"Status": "OK", "Message": "Action recorded", "Action outcome": action.outcome}


def invalid_action(available_actions, requested_action):
    return {
        "Status": "Error",
        "Message": "Invalid action",
        "Action": requested_action,
        "Available actions": ", ".join(str(action) for action in available_actions)}


@get('/games/new/<player1>/vs/<player2>')
def new_game(player1, player2):
    games = get_games_db()
    player1 = Player("Green", player1)
    player2 = Player("Red", player2)

    player1.ai_name = "Human"
    player2.ai_name = "Human"

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1, player1_units, player2, player2_units)

    game_id = games.insert(gamestate.to_document())

    return {"Status": "OK", "ID": str(game_id), "ServerTime": time.time()}


def get_current_gamestate(game_document, actions=None):
    gamestate = Gamestate.from_document(game_document)

    if not actions:
        actions = get_actions_db().find({"game": ObjectId(game_document["_id"])}).sort("action_number")

    for action_document in actions:
        action_with_references = get_action(gamestate, action_document)
        action_with_references.ensure_outcome(action_document["outcome"])
        gamestate.do_action(action_with_references)
        gamestate.shift_turn_if_done()

    return gamestate


def get_games_db():
    client = MongoClient()
    database = client.unnamed
    return database.games


def get_actions_db():
    client = MongoClient()
    database = client.unnamed
    return database.actions


host_address = "10.224.105.151"
if socket.gethostname() == "MD-rMBP.local":
    host_address = "localhost"

install(JSONPlugin(json_dumps=lambda s: dumps(s, cls=CustomJsonEncoder)))
run(host=host_address, port=8080, debug=True)
