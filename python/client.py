import json
import urllib2
from common import *
from action import Action
from outcome import Outcome
from datetime import datetime
import setup_settings as settings
from time import sleep


class Client():
    def __init__(self, profilename, game_id=None):
        self.profilename = profilename
        self.game_id = game_id

    def get_game(self):
        if self.game_id:
            return json.load(urllib2.urlopen(settings.server + "/games/view/" + self.game_id))

        else:
            response = json.load(urllib2.urlopen(settings.server + "/games/join_or_create/" + self.profilename))
            self.game_id = response["ID"]

            print response["Message"], self.game_id

            return self.get_game()

    def select_action(self, gamestate):
        game = self.get_game()
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
            opponent = self.look_for_opponent()
            if opponent:
                print "Opponent found:", opponent_descriptions
            print "Waiting for opponent..."
            sleep(1000)

    def look_for_opponent(self):
        game = self.get_game()
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
