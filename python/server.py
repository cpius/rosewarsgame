from bottle import run, get, post, install, JSONPlugin, request
from pymongo import MongoClient
from bson import ObjectId
import socket
import time
from datetime import datetime
from gamestate import Gamestate
from game import Game
from action import Action
from player import Player
import setup
from common import Trait, document_to_string, Position
from outcome import Outcome


@get('/games/view/<game_id>')
def view(game_id):
    games = get_collection("games")
    game_document = games.find_one({"_id": ObjectId(game_id)})
    if not game_document:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    actions = get_collection("actions")
    action_documents = actions.find({"game": ObjectId(game_id)}).sort("number")

    log_document = construct_log_document(game_document, action_documents)
    gamestate = Gamestate.from_log_document(log_document, shift_turn=True)

    return gamestate.to_document()


@get("/actions/view/<game_id>")
def view_actions(game_id):
    actions = get_collection("actions")
    action_documents = list(actions.find({"game": ObjectId(game_id)}))
    actions_document = dict()
    if len(action_documents) > 0:
        actions_document["last_action"] = action_documents[-1]["number"]
        actions_document["last_updated_at"] = action_documents[-1]["created_at"]

    for action in action_documents:
        actions_document[action["number"]] = action

    return actions_document


@post('/games/<game_id>/do_action')
def do_action_post(game_id):
    games = get_collection("games")
    game_document = games.find_one({"_id": ObjectId(game_id)})
    if not game_document:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    action_documents = list(get_collection("actions").find({"game": ObjectId(game_id)}).sort("number"))

    log_document = construct_log_document(game_document, action_documents)

    gamestate = Gamestate.from_log_document(log_document, shift_turn=True)

    try:
        action_document = request.json
    except ValueError:
        return {"Status": "Error", "Message": "No JSON decoded. Request body: " + request.body.getvalue()}

    expected_number, expected_type = get_expected_action(log_document, gamestate)
    print "expecting", expected_number, expected_type
    if action_document["type"] == "action":
        action_type = "action"
    elif "move_with_attack" in action_document:
        action_type = "move_with_attack"
    elif "upgrade" in action_document:
        action_type = "upgrade"
    else:
        raise Exception("Unknown action type " + document_to_string(action_document))
    if action_type != expected_type or expected_number != action_document["number"]:
        message = "The next action must have type " + expected_type + " and have number " + str(expected_number)
        return {"Status": "Error", "Message": message}

    action_collection = get_collection("actions")

    if action_document["type"] == "options":
        action_document["game"] = ObjectId(game_id)
        action_collection.insert(action_document)
        return {"Status": "OK", "Message": "Options recorded"}

    # When playing locally, this is set continuously. We have to set it manually
    gamestate.set_available_actions()

    available_actions = gamestate.get_actions_with_none()

    if Position.from_string(action_document["start_at"]) not in gamestate.player_units:
        return invalid_action(available_actions, request.json)

    action = Action.from_document(gamestate.all_units(), action_document)

    if not action:
        return invalid_action(available_actions, request.json)

    if not action in available_actions:
        return invalid_action(available_actions, str(action))

    gamestate_before = gamestate.copy()

    outcome = None
    if action.is_attack():
        outcome = Outcome.determine_outcome(action, gamestate)
    gamestate.do_action(action, outcome)
    if gamestate.is_turn_done():
        gamestate.shift_turn()
    action_document["game"] = ObjectId(game_id)
    action_collection.insert(action_document)
    outcome_document = outcome.to_document()
    outcome_document["game"] = ObjectId(game_id)
    outcome_document["type"] = "outcome"
    outcome_document["number"] = action.number
    action_collection.insert(outcome_document)

    response = {
        "Status": "OK",
        "Message": "Action recorded",
        "Available actions": [str(action) for action in available_actions],
        "Gamestate before": gamestate_before.to_document(),
        "Gamestate after": gamestate.to_document()
    }

    if action.is_attack():
        response["Action outcome"] = outcome.to_document()

    return response


def get_expected_action(log_document, gamestate):
    action_number = log_document["action_count"]
    if action_number == 0:
        return 1, "action"

    last_action_document = log_document[str(action_number)]

    last_action_options = None
    if str(action_number) + "_options" in log_document:
        last_action_options = log_document[str(action_number) + "_options"]

    if not "move_with_attack" in last_action_document:
        if not last_action_options or not "move_with_attack" in last_action_options:
            return action_number, "move_with_attack"

    unit_position = Position.from_string(last_action_document["end_at"])
    if not unit_position in gamestate.all_units():
        unit_position = Position.from_string(last_action_document["target_at"])

    if gamestate.all_units()[unit_position].is_milf():
        if not last_action_options or not "upgrade" in last_action_options:
            return action_number, "upgrade"

    return action_number + 1, "action"


def invalid_action(available_actions, requested_action):
    return {
        "Status": "Error",
        "Message": "Invalid action",
        "Action": requested_action,
        "Available actions": ", ".join(str(action) for action in available_actions)}


@get('/games/new/<player1>/vs/<player2>')
def new_game(player1, player2):
    games = get_collection("games")
    players = [Player("Green", "Human", player1), Player("Red", "Human", player2)]

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1_units, player2_units, 1, False, datetime.utcnow())

    game = Game(players, gamestate)
    game_id = games.insert(game.to_document())

    return {"Status": "OK", "ID": str(game_id), "ServerTime": time.time()}


def get_collection(collection):
    client = MongoClient()
    database = client.unnamed

    return getattr(database, collection)


def construct_log_document(game_document, action_documents):
    replay_document = game_document.copy()
    action_count = 0
    for action_document in action_documents:
        key = str(action_document["number"])
        if int(key) > action_count:
            action_count = int(key)
        if action_document["type"] == "outcome":
            key += "_outcome"
        elif action_document["type"] == "options":
            key += "_options"
        action_log = action_document.copy()
        del action_log["number"]
        del action_log["type"]
        replay_document[key] = action_log
    replay_document["action_count"] = action_count

    return replay_document


host_address = "10.224.105.151"
if socket.gethostname() == "MD-rMBP.local":
    host_address = "localhost"

install(JSONPlugin(json_dumps=lambda document: document_to_string(document)))
run(host=host_address, port=8080, debug=True)
