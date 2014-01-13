import json
import urllib2
from common import *
from action import Action
from outcome import Outcome
from datetime import datetime
import setup_settings as settings


class Client():
    def __init__(self, game_id):
        self.game_id = game_id

    def get_game(self):
        return json.load(urllib2.urlopen(settings.server + "/games/view/" + self.game_id))

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
                        enumified_upgrade = {}
                        for key, value in upgrade.iteritems():
                            if hasattr(Trait, key):
                                enumified_upgrade[getattr(Trait, key)] = value
                            elif hasattr(Ability, key):
                                enumified_upgrade[getattr(Trait, key)] = value
                        upgrade = enumified_upgrade

            return action, outcome, upgrade

        return None, None, None

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
