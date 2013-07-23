import json
import urllib2
from gamestate_module import Gamestate
from time import sleep
from methods import CustomJsonEncoder
from action import Action


class Client():
    server = "http://localhost:8080"

    def __init__(self, game_id):
        self.game_id = game_id

    def get_gamestate(self):
        return Gamestate.from_document(
            json.load(
                urllib2.urlopen(self.server + "/games/view/" + self.game_id)))

    def select_action(self, last_known_action):
        expected_action = last_known_action + 1
        while True:
            url = self.server + "/actions/view/" + self.game_id
            print "Getting action from: " + url
            print "last known action: " + str(last_known_action)
            actions = json.load(urllib2.urlopen(url))
            if "last_action" in actions and actions["last_action"] > last_known_action:
                print "found new action. returning"
                print Action.from_document(actions[str(expected_action)])
                return Action.from_document(actions[str(expected_action)])
            print "No new actions. Sleeping for one second"
            sleep(1)

    def send_action(self, action):
        data = urllib.urlencode(action)
        url = self.server + "/games/" + self.game_id + "/do_action"
        response = json.load(urllib2.urlopen(url, data))
        if response["Status"] == "OK":
            return True
        else:
            return False




# print "Polling for actions with number higher than 2"
# client = Client()
# all_actions = client.poll_actions("51ed68bad288595ed139d274", 2)
# print "Found new action(s)!"
# pp = PrettyPrinter()
# print pp.pformat(all_actions)
# print [pp.pformat(data) for data in all_actions if isinstance(data, dict)]
