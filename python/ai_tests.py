from gamestate import Gamestate
from action import Action
import json
import ai_level2 as ai

path = "../ai_tests/test1.json"
document = json.loads(open(path).read())

gamestate = Gamestate.from_document(document["gamestate"])
desired_action = Action.from_document(gamestate.all_units(), document["action"])
gamestate.set_available_actions()
actions = gamestate.get_actions()

action = ai.get_action(actions, gamestate)

print action
print desired_action
print action == desired_action
