import json
from gamestate_module import Gamestate
from action import Action
import action_getter
import battle
import common
from outcome import Outcome


def run_utest(utest):
    if utest["Type"] == "Does action exist":
        gamestate = Gamestate.from_document(utest["Gamestate"])
        action = Action.from_document_simple(utest["Action"])
        return (action in action_getter.get_actions(gamestate)) == utest["Result"]

    if utest["Type"] == "Is attack and defence correct":
        gamestate = Gamestate.from_document(utest["Gamestate"])
        action = Action.from_document(utest["Action"])

        all_units = common.merge_units(gamestate.units[0], gamestate.units[1])

        attacking_unit = all_units[action.start_position]
        defending_unit = all_units[action.attack_position]

        attack = battle.get_attack_rating(attacking_unit, defending_unit, action)
        defence = battle.get_defence_rating(attacking_unit, defending_unit, attack)

        return (attack == int(utest["Attack"])) and (defence == int(utest["Defence"]))

    if utest["Type"] == "Is outcome correct":
        actual_gamestate = Gamestate.from_document(utest["Gamestate before action"])
        post_gamestate = Gamestate.from_document(utest["Gamestate after action"])
        action = Action.from_document_simple(utest["Action"])
        outcome = Outcome.from_document(utest["Outcome"])
        actual_gamestate.do_action(action, outcome)

        actual_gamestate_document = actual_gamestate.to_document()
        post_gamestate_document = post_gamestate.to_document()

        return actual_gamestate_document == post_gamestate_document


utest = json.loads(open("./utests/Is_outcome_correct_" + str(1) + ".utest").read())
print run_utest(utest)


for i in range(1, 2):
    utest = json.loads(open("./utests/Is_attack_and_defence_correct_" + str(i) + ".json").read())
    print run_utest(utest)


for i in range(1, 3):
    utest = json.loads(open("./utests/Does_action_exist_" + str(i) + ".json").read())
    print run_utest(utest)
