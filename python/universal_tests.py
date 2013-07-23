import json
from gamestate_module import Gamestate
from action import Action
import action_getter


def run_utest(utest):
    if utest["Type"] == "Does action exist":
        gamestate = Gamestate.from_document(utest["Gamestate"])
        action = Action.from_document(utest["Action"])
        return (action in action_getter.get_actions(gamestate)) == utest["Result"]


for i in range(1, 3):
    utest = json.loads(open("./utests/Does_action_exist_" + str(i) + ".json").read())
    print run_utest(utest)


