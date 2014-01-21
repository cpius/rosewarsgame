import json
import urllib2
from common import *
from action import Action
from outcome import Outcome
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time
from email.utils import parsedate
import setup_settings as settings
from time import sleep


class DefaultErrorHandler(urllib2.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, headers):
        result = urllib2.HTTPError(req.get_full_url(), code, msg, headers, fp)
        result.status = code

        return result


class Client():
    def __init__(self, profilename, game_id=None):
        self.profilename = profilename
        self.game_id = game_id
        self.last_modified = datetime(1970, 1, 1)

    def get_game(self):
        if self.game_id:
            print "getting game from server"
            request = urllib2.Request(settings.server + "/games/view/" + self.game_id)

            stamp = mktime(self.last_modified.timetuple())
            formatted_time = format_date_time(stamp)
            if self.last_modified > datetime(1970, 1, 1):
                print "setting If-Modified-Since", formatted_time
                request.add_header("If-Modified-Since", formatted_time)

            opener = urllib2.build_opener(DefaultErrorHandler())
            response = opener.open(request)
            if response.getcode() == 304:
                print "no new data on the server"
                return

            last_modified_header = response.info().getheader("Last-Modified")
            if last_modified_header:
                last_modified_tuple = parsedate(last_modified_header)
                last_modified_timestamp = mktime(last_modified_tuple)
                last_modified = datetime.fromtimestamp(last_modified_timestamp)

                print "response Last-Modified: ", last_modified

                if last_modified > self.last_modified:
                    print "new data was found on the server"
                    self.last_modified = last_modified
                else:
                    print "no new data on the server"
                    return

            return json.load(response)

        else:
            response = json.load(urllib2.urlopen(settings.server + "/games/join_or_create/" + self.profilename))
            self.game_id = response["ID"]

            print response["Message"], self.game_id

            if response["Message"] == "New game created":
                return self.wait_for_opponent()
            else:
                return self.get_game()

    def select_action(self, gamestate):
        game = self.get_game()
        if not game:
            # No new data on the server
            return None, None, None
        expected_action = str(gamestate.action_count + 1)

        if game["action_count"] > gamestate.action_count:
            print "received action", document_to_string(game[expected_action])
            action = Action.from_document(gamestate.all_units(), game[expected_action])
            outcome = None
            if action.is_attack():
                outcome = Outcome.from_document(game[expected_action + "_outcome"])

            upgrade = None
            if expected_action + "_options" in game:
                options = game[expected_action + "_options"]
                if "move_with_attack" in options:
                    action.move_with_attack = bool(options["move_with_attack"])
                if "upgrade" in options:
                    upgrade = options["upgrade"]
                    if not isinstance(upgrade, basestring):
                        upgrade = enum_attributes(upgrade)

            return action, outcome, upgrade

        return None, None, None

    def wait_for_opponent(self):
        while True:
            game = self.get_game()
            opponent = self.look_for_opponent(game)
            if opponent:
                print "Opponent found:", opponent
                return game
            print "Waiting for opponent..."
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
        url = settings.server + "/games/" + self.game_id + "/do_action"
        print "sending json:", document_to_string(action)
        request = urllib2.Request(url, document_to_string(action), {"Content-Type": "application/json"})
        response = urllib2.urlopen(request)
        response_string = response.read()
        print "received: " + response_string
        json_response = json.loads(response_string)
        response.close()
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
