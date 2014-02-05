from gamestate import Gamestate
from action import Action
import json
import ai as ai_module
import glob

paths = glob.glob("../ai_tests/*.json")

for path in paths:
    print path
    document = json.loads(open(path).read())

    gamestate = Gamestate.from_document(document["gamestate"])
    desired_action = Action.from_document(gamestate.all_units(), document["action"])

    gamestate.set_available_actions()
    ai = ai_module.AI()

    action = ai.select_action(gamestate)

    if action != desired_action:
        print action
        print desired_action
        print
