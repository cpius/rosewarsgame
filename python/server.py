from bottle import run, get, post, install, JSONPlugin, request, response
from pymongo import MongoClient
import socket
from time import mktime, time
from wsgiref.handlers import format_date_time
from email.utils import parsedate
from gamestate import Gamestate
from game import Game
from action import Action
from player import Player
import setup
from common import *
from outcome import Outcome
import random
import memcache
import traceback

cache = memcache.Client(['127.0.0.1:11211'], debug=0)


@get("/games/new/<player1>/vs/<player2>")
def new_game(player1, player2):
    games = get_collection("games")
    players = [Player("Green", "Human", player1), Player("Red", "Human", player2)]

    player1_units, player2_units = setup.get_start_units()

    gamestate = Gamestate(player1_units, player2_units, 1, False, datetime.utcnow())

    game = Game(players, gamestate)
    game_id = games.insert(game.to_document())

    return {"Status": "OK", "ID": str(game_id), "ServerTime": time(), "Message": "New game created"}


@get("/games/view/<game_id>")
def view(game_id):
    last_modified_cache = cache.get(game_id)
    if last_modified_cache:
        if_modified_since_header = request.get_header("If-Modified-Since")
        if if_modified_since_header:
            if_modified_since_tuple = parsedate(if_modified_since_header)
            if_modified_since_timestamp = mktime(if_modified_since_tuple)
            if_modified_since = datetime.fromtimestamp(if_modified_since_timestamp)
            if last_modified_cache <= if_modified_since:
                # If our latest update is earlier than the client's latest update,
                # let the client know that nothing new is afoot
                response.status = 304
                return

    games = get_collection("games")
    game_document = games.find_one({"_id": ObjectId(game_id)})
    if not game_document:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    log_document = construct_log_document(game_document)
    game = Game.from_log_document(log_document)
    number = get_expected_action(log_document, game.gamestate)[0]
    if number == log_document["action_count"]:
        # Action isn't completed yet
        log_document["action_count"] = number - 1

    last_modified = log_document["last_modified"]
    if last_modified > datetime(1970, 1, 1):
        stamp = mktime(last_modified.timetuple())
        formatted_time = format_date_time(stamp)
        response.set_header("Last-Modified", formatted_time)
        cache.set(game_id, last_modified.replace(microsecond=0))

    return log_document


@get("/cache/get/<game_id>")
def getcache(game_id):
    return str(cache.get(game_id))


@get("/games/view_log/<game_id>")
def view_log(game_id):
    games = get_collection("games")
    game_document = games.find_one({"_id": ObjectId(game_id)})
    if not game_document:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    log_document = construct_log_document(game_document)

    return log_document


@get("/actions/view/<game_id>")
def view_actions(game_id):
    actions = get_collection("actions")
    action_documents = list(actions.find({"game": ObjectId(game_id)}))
    actions_document = dict()
    if len(action_documents) > 0:
        main_actions = [main_action for main_action in action_documents if main_action["type"] == "action"]
        actions_document["last_action"] = main_actions[-1]["number"]
        actions_document["last_updated_at"] = main_actions[-1]["created_at"]

    for action in action_documents:
        actions_document[action["number"]] = action

    return actions_document


# db.games.update({}, { "$set": { "finished_at": finished_at } }, {"multi": true} );
@get("/games/join_or_create/<profile>")
def join_or_create(profile):
    games = get_collection("games")

    ongoing_games = list(games.find(
        {
            "$and": [
                {"finished_at": None},
                {"$or": [{"player1.profile": profile}, {"player2.profile": profile}]}]
        }))
    if ongoing_games:
        return {
            "Status": "OK",
            "ID": ongoing_games[0]["_id"],
            "ServerTime:": time(),
            "Message": "Joined ongoing game"
        }

    open_games = list(games.find(
        {
            "$and": [
                {
                    "$and": [
                        {"player1.profile": {"$ne": profile}},
                        {"player2.profile": {"$ne": profile}}
                    ]
                },
                {
                    "$or": [
                        {"player1.profile": "OPEN"},
                        {"player2.profile": "OPEN"}
                    ]
                }
            ]
        }))
    if open_games:
        game_to_join = open_games[0]
        if game_to_join["player1"]["profile"] == "OPEN":
            game_to_join["player1"]["profile"] = profile
        else:
            game_to_join["player2"]["profile"] = profile
        games.save(game_to_join)

        return {"Status": "OK", "ID": game_to_join["_id"], "ServerTime": time(), "Message": "Joined existing game"}

    if random.randint(0, 1) == 0:
        return new_game(profile, "OPEN")
    else:
        return new_game("OPEN", profile)


@post("/games/<game_id>/do_action")
def do_action_post(game_id):
    games = get_collection("games")
    game_document = games.find_one({"_id": ObjectId(game_id)})
    if not game_document:
        return {"Status": "Error", "Message": "Could not find game with id " + game_id}

    try:
        action_document = request.json
    except ValueError:
        return {"Status": "Error", "Message": "No JSON decoded. Request body: " + request.body.getvalue()}

    action_document["created_at"] = datetime.utcnow()
    log_document = construct_log_document(game_document)
    game = Game.from_log_document(log_document)

    validation_errors = validate_input(log_document, game.gamestate, action_document)
    if validation_errors:
        return validation_errors

    if action_document["type"] == "options" and "move_with_attack" in action_document:
        response_document = register_move_with_attack(action_document, game_id)
        cache.set(game_id, datetime.utcnow().replace(microsecond=0))
        return response_document
    elif action_document["type"] == "options" and "upgrade" in action_document:
        response_document = register_upgrade(action_document, game.gamestate, game_id)
        cache.set(game_id, datetime.utcnow().replace(microsecond=0))
        return response_document

    # Initial validation is done with a non-shifted gamestate, because it is
    # easier to find expected action from that
    # The rest is done with the turn shifted (if relevant)
    if game.is_turn_done():
        game.shift_turn()

    result = validate_action(game.gamestate, action_document)
    if isinstance(result, dict):
        return result
    else:
        action = result

    response_document = register_move_attack_ability(action_document, game_id, game.gamestate, action)
    cache.set(game_id, datetime.utcnow().replace(microsecond=0))
    return response_document


@get("/ranking/calculate")
def calculate_ratings():
    games = list(get_collection("games").find({}).sort("finished_at", 1))

    debug_lines = []
    ranking = {}

    try:
        for game_document in games:
            log_document = construct_log_document(game_document)
            game = Game.from_log_document(log_document)
            if game.gamestate.is_ended():
                winner = game.current_player().profile
                loser = game.opponent_player().profile
                if not winner in ranking:
                    ranking[winner] = 1000
                if not loser in ranking:
                    ranking[loser] = 1000

                rating_difference = ranking[loser] - ranking[winner]

                # "skill_factor" is an expression I came up with. I'm not sure what it's really called.
                # Arpad Elo came up with the value 400. It means that a player with 400 higher rating
                # than another player has a 90% probability of winning. At a difference of 200 the
                # probability is 75%
                skill_factor = float(2000)

                expected_outcome_for_winner = 1 / (1 + pow(10, (rating_difference / skill_factor)))

                # The k value determines the volatility in the ratings. 32 is pretty high. It's what ICC uses
                # It means that the most points that can be won in one game is 32
                k_value = 32

                rating_points_won_and_lost = int(k_value * (1 - expected_outcome_for_winner))

                debug_line = str(game_document["_id"]) + ": " + winner + " beat " + loser
                debug_line += " (probability: " + "{0:.2f}".format(expected_outcome_for_winner) + "). "
                debug_line += winner + ": " + str(ranking[winner])
                debug_line += " => " + str(ranking[winner] + rating_points_won_and_lost) + ", "
                debug_line += loser + ": " + str(ranking[loser])
                debug_line += " => " + str(ranking[loser] - rating_points_won_and_lost)
                debug_lines.append(debug_line)

                ranking[winner] += rating_points_won_and_lost
                ranking[loser] -= rating_points_won_and_lost
    except Exception:
        debug_lines.append(traceback.format_exc())

    for index, line in enumerate(debug_lines):
        ranking["debug_{0:03d}".format(index)] = line

    return ranking


def register_upgrade(action_document, gamestate, game_id):
    position, unit = gamestate.get_upgradeable_unit()

    upgrade_options = [unit.get_upgrade_choice(0), unit.get_upgrade_choice(1)]
    is_valid_choice = False

    is_simple_upgrade = isinstance(action_document["upgrade"], basestring)

    for choice in range(0, 2):
        if is_simple_upgrade:
            if upgrade_options[choice] == upgrade_options[choice]:
                is_valid_choice = True
        else:
            if action_document["upgrade"] == readable(upgrade_options[choice]):
                is_valid_choice = True
    if not is_valid_choice:
        message = "The upgrade must be one of "
        for choice in range(0, 2):
            if isinstance(upgrade_options[choice], basestring):
                message += upgrade_options[choice]
            else:
                message += str(readable(upgrade_options[0]))
            if choice == 0:
                message += " and "

        return {"Status": "Error", "Message": message}

    if is_simple_upgrade:
        new_unit = unit.get_upgraded_unit(action_document["upgrade"])
    else:
        new_unit = unit.get_upgraded_unit(enum_attributes(action_document["upgrade"]))

    action_collection = get_collection("actions")

    existing_options = action_collection.find_one(
        {"type": "options", "number": action_document["number"], "game": ObjectId(game_id)})
    if existing_options:
        existing_options["upgrade"] = action_document["upgrade"]
        action_collection.save(existing_options)
    else:
        action_document["game"] = ObjectId(game_id)
        action_collection.insert(action_document)

    return {
        "Status": "OK",
        "Message": "Upgraded " + str(unit) + " on " + str(position),
        "New unit": document_to_string(new_unit.to_document())}


def register_move_with_attack(action_document, game_id):
    action_collection = get_collection("actions")

    action_document["game"] = ObjectId(game_id)
    action_collection.insert(action_document)
    return {"Status": "OK", "Message": "Options recorded"}


def register_move_attack_ability(action_document, game_id, gamestate, action):
    # gamestate_before = gamestate.copy()
    outcome = None

    if action.is_attack():
        outcome = Outcome.determine_outcome(action, gamestate)

    gamestate.do_action(action, outcome)

    if gamestate.is_ended():
        games = get_collection("games")
        games.update({"_id": ObjectId(game_id)}, {"$set": {"finished_at": datetime.utcnow()}})

    if action.move_with_attack is None and action.target_at in gamestate.enemy_units:
        # The outcome ruled out the possibility of move-with-attack
        action.move_with_attack = False

    if gamestate.is_turn_done():
        gamestate.shift_turn()

    action_collection = get_collection("actions")

    action_document["game"] = ObjectId(game_id)

    if not "move_with_attack" in action_document and action.move_with_attack in [True, False]:
        # The client may send nothing rather than specify the default value (False)
        # In that case, make sure the default is saved to the database
        action_document["move_with_attack"] = action.move_with_attack

    action_collection.insert(action_document)

    response_document = {
        "Status": "OK",
        "Message": "Action recorded"
        # "Available actions": [str(available_action) for available_action in available_actions],
        # "Gamestate before": gamestate_before.to_document(),
        # "Gamestate after": gamestate.to_document()
    }

    if outcome:
        outcome_document = outcome.to_document()
        outcome_document["game"] = ObjectId(game_id)
        outcome_document["type"] = "outcome"
        outcome_document["number"] = action.number
        outcome_document["created_at"] = action_document["created_at"]

        action_collection.insert(outcome_document)

        response_document["Action outcome"] = outcome.to_document()

    return response_document


def validate_input(log_document, gamestate, action_document):
    expected_number, expected_type = get_expected_action(log_document, gamestate)

    if action_document["type"] == "action":
        action_type = "action"
    elif "move_with_attack" in action_document:
        action_type = "move_with_attack"
    elif "upgrade" in action_document:
        action_type = "upgrade"
    else:
        raise Exception("Unknown action type " + document_to_string(action_document))
    if action_type != expected_type or expected_number != int(action_document["number"]):
        message = "The next action must have type " + expected_type + " and have number " + str(expected_number)
        return {"Status": "Error", "Message": message}


def validate_action(gamestate, action_document):

    gamestate.set_available_actions()
    available_actions = gamestate.get_actions_with_none()

    if Position.from_string(action_document["start_at"]) not in gamestate.player_units:
        return invalid_action(available_actions, request.json)

    action = Action.from_document(gamestate.all_units(), action_document)

    if not action:
        return invalid_action(available_actions, request.json)

    if not action in available_actions:
        return invalid_action(available_actions, str(action))

    return action


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

    unit, position = gamestate.get_unit_from_action_document(last_action_document)
    if unit.should_be_upgraded():
        if not last_action_options or not "upgrade" in last_action_options:
            return action_number, "upgrade",

    return action_number + 1, "action"


def invalid_action(available_actions, requested_action):
    return {
        "Status": "Error",
        "Message": "Invalid action",
        "Action": requested_action,
        "Available actions": ", ".join(str(action) for action in available_actions)}


def get_collection(collection):
    client = MongoClient()
    database = client.unnamed

    return getattr(database, collection)


def construct_log_document(game_document):
    actions = get_collection("actions")
    action_documents = actions.find({"game": ObjectId(game_document["_id"])}).sort("number")

    replay_document = game_document.copy()
    action_count = 0
    last_modified = datetime(1970, 1, 1)
    for action_document in action_documents:
        key = str(action_document["number"])

        if int(key) > action_count:
            action_count = int(key)

        if "created_at" in action_document:
            created_at = action_document["created_at"]
            if isinstance(created_at, unicode):
                try:
                    created_at = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
                except ValueError:
                    if "." in created_at:
                        created_at = created_at[0:created_at.index(".")]
                    created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")

            if created_at > last_modified:
                last_modified = created_at

        if action_document["type"] == "outcome":
            key += "_outcome"
        elif action_document["type"] == "options":
            key += "_options"
        action_log = action_document.copy()
        del action_log["number"]
        del action_log["type"]
        replay_document[key] = action_log

    replay_document["action_count"] = action_count
    replay_document["last_modified"] = last_modified

    return replay_document


host_address = "10.224.105.151"
if socket.gethostname() == "MD-rMBP.local":
    host_address = "localhost"

install(JSONPlugin(json_dumps=lambda document: document_to_string(document)))
run(host=host_address, port=8080, debug=True)
