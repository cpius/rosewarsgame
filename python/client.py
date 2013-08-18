import json
import urllib2
from gamestate import Gamestate
from common import document_to_string
from action import Action
from outcome import Outcome
from datetime import datetime


class Client():
    # server = "http://localhost:8080"
    server = "http://server.rosewarsgame.com:8080"

    def __init__(self, game_id):
        self.game_id = game_id

    def get_gamestate(self):
        return Gamestate.from_document(
            json.load(
                urllib2.urlopen(self.server + "/games/view/" + self.game_id)))

    def get_game(self):
        return json.load(urllib2.urlopen(self.server + "/games/view/" + self.game_id))

    def select_action(self, gamestate):
        game = self.get_game()
        expected_action = str(gamestate.action_count + 1)

        if game["action_count"] > gamestate.action_count:
            print "received action", document_to_string(game[expected_action])
            action = Action.from_document(gamestate.all_units(), game[expected_action])
            if action.is_attack():
                outcome = Outcome.from_document(game[expected_action + "_outcome"])
                return action, outcome

            return action, None

        print "No new actions. Sleeping for one second"
        return None, None

        url = self.server + "/games/" + self.game_id + "/do_action"
        print "sending json: " + json.dumps(action, cls=CustomJsonEncoder)
        request = urllib2.Request(url, json.dumps(action, cls=CustomJsonEncoder), {"Content-Type": "application/json"})
        response = urllib2.urlopen(request)
        response_string = response.read()
        print "received: " + response_string
        json_response = json.loads(response_string)
        response.close()
        if json_response["Status"] == "OK":
            return json_response["Action outcome"] == "Success"


# print "Polling for actions with number higher than 2"
# client = Client()
# all_actions = client.poll_actions("51ed68bad288595ed139d274", 2)
# print "Found new action(s)!"
# pp = PrettyPrinter()
# print pp.pformat(all_actions)
# print [pp.pformat(data) for data in all_actions if isinstance(data, dict)]
