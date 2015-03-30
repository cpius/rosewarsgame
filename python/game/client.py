import requests
from gamestate.gamestate_library import *
from gamestate.action import Action
from gamestate.outcome import Outcome
from datetime import datetime
from time import mktime, sleep
from email.utils import parsedate
from game.game_library import document_to_string
from game.settings import server


class Client():
    def __init__(self, profilename, game_id=None):
        self.profilename = profilename
        self.game_id = game_id
        self.last_modified = datetime(1970, 1, 1)

    def get_game(self):
        if self.game_id:
            request_headers = {}

            formatted_time = httpdate(self.last_modified)
            if self.last_modified > datetime(1970, 1, 1):
                request_headers["If-Modified-Since"] = formatted_time

            response = requests.get(server + "/games/view/" + self.game_id, headers=request_headers)

            if response.status_code == 304:
                return

            if "last-modified" in response.headers:
                last_modified_header = response.headers["last-modified"]
                last_modified_tuple = parsedate(last_modified_header)
                last_modified_timestamp = mktime(last_modified_tuple)
                last_modified = datetime.fromtimestamp(last_modified_timestamp)

                if last_modified > self.last_modified:
                    self.last_modified = last_modified
                else:
                    return

            return response.json()

        else:
            response = requests.get(server + "/games/join_or_create/" + self.profilename).json()
            self.game_id = response["ID"]

            print(response["Message"], self.game_id)

            if response["Message"] == "New game created":
                return self.wait_for_opponent()
            else:
                return self.get_game()

    def select_action(self, gamestate):
        game = self.get_game()
        if not game:
            print("No new data on the server. By the way, our last update was from", self.last_modified)
            # No new data on the server
            return None, None, None
        expected_action = str(gamestate.action_count + 1)

        if game["action_count"] > gamestate.action_count + 1:
            # Several new things happened on the server
            # Handle this one now, but clear last_modified to make
            # sure we hear about the other stuff
            self.last_modified = datetime(1970, 1, 1)

        if game["action_count"] > gamestate.action_count:
            print("received action", document_to_string(game[expected_action]))
            action = Action.from_document(gamestate.all_units(), game[expected_action])
            outcome = None
            if action.is_attack:
                outcome = Outcome.from_document(game[expected_action + "_outcome"])

            upgrade = None
            if expected_action + "_options" in game:
                options = game[expected_action + "_options"]
                if "move_with_attack" in options:
                    action.move_with_attack = bool(options["move_with_attack"])
                if "upgrade" in options:
                    upgrade = get_enum_attributes(options["upgrade"])

            return action, outcome, upgrade

        return None, None, None

    def wait_for_opponent(self):
        while True:
            game = self.get_game()
            opponent = self.look_for_opponent(game)
            if opponent:
                print("Opponent found:", opponent)
                return game
            print("Waiting for opponent...")
            sleep(3)

    def look_for_opponent(self, game):
        player1 = game["player1"]["profile"]
        player2 = game["player2"]["profile"]
        if player1 != self.profilename and player1 != "OPEN":
            return player1
        elif player2 != self.profilename and player2 != "OPEN":
            return player2

        return

    def send_action(self, action):
        url = server + "/games/" + self.game_id + "/do_action"
        print("sending json:", document_to_string(action))
        request = requests.post(url, data=document_to_string(action), headers={"Content-Type": "application/json"})
        print("received: " + request.text)
        json_response = request.json()
        if json_response["Status"] == "OK":
            if "Action outcome" in json_response:
                return Outcome.from_document(json_response["Action outcome"])
        else:
            raise Exception("Unexpected response: " + document_to_string(json_response))

    def send_move_with_attack(self, move_with_attack, number):
        move_with_attack_action = {
            "number": number,
            "created_at": datetime.utcnow(),
            "type": "options",
            "move_with_attack": move_with_attack
        }
        self.send_action(move_with_attack_action)

    def send_upgrade_choice(self, upgrade_choice, number):
        upgrade_action = {
            "number": number,
            "created_at": datetime.utcnow(),
            "type": "options",
            "upgrade": upgrade_choice
        }
        self.send_action(upgrade_action)


def httpdate(dt):
    """Return a string representation of a date according to RFC 1123
    (HTTP/1.1).

    The supplied date must be in UTC.

    """
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    rfc1123_format = "%s, %02d %s %04d %02d:%02d:%02d GMT"

    return rfc1123_format % (weekday, dt.day, month, dt.year, dt.hour, dt.minute, dt.second)
