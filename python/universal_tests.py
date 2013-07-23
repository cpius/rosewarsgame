import json
from gamestate_module import Gamestate
from action import Action
import action_getter
import battle
import methods


def run_utest(utest):
    if utest["Type"] == "Does action exist":
        gamestate = Gamestate.from_document(utest["Gamestate"])
        action = Action.from_document(utest["Action"])
        return (action in action_getter.get_actions(gamestate)) == utest["Result"]

    if utest["Type"] == "Is attack and defence correct":
        gamestate = Gamestate.from_document(utest["Gamestate"])
        action = Action.from_document(utest["Action"])

        all_units = methods.merge_units(gamestate.units[0], gamestate.units[1])

        attacking_unit = all_units[action.start_position]
        defending_unit = all_units[action.attack_position]

        attack = battle.get_attack_rating(attacking_unit, defending_unit, action)
        defence = battle.get_defence_rating(attacking_unit, defending_unit, attack)

        return (attack == int(utest["Attack"])) and (defence == int(utest["Defence"]))


for i in range(1, 2):
    utest = json.loads(open("./utests/Is_attack_and_defence_correct_" + str(i) + ".json").read())
    print run_utest(utest)

