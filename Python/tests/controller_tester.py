from gamestate.gamestate_module import Gamestate, Position
import glob
from collections import namedtuple
from game.game_module import Game
from controller import Controller
from gamestate.outcome import Outcome
from functools import partial
from tests.dictdiffer import DictDiffer
from gamestate.action import Action
from tests.test_library import *

rolls = namedtuple("rolls", ["attack", "defence"])


class View:
    def draw_game(self, *args, **kwargs):
        pass

    def draw_action(self, *args, **kwargs):
        pass

    def save_screenshot(self, *args, **kwargs):
        pass

    def shade_positions(self, *args, **kwargs):
        pass

    def draw_ask_about_move_with_attack(self, *args, **kwargs):
        pass

    def draw_post_movement(*args):
        pass


class Sound:
    def play_fanfare(self):
        pass

    def play_action(self, *args):
        pass


def determine_outcome(outcome, *args):
    return outcome


def pick_end_at(end_at, *args):
    return end_at


def add_log(*args):
    pass


def ask_about_move_with_attack(answer, *args):
    return answer


def save(*args):
    pass


def give_output(actual_gamestate, expected_gamestate, actual_positions, expected_positions):

    if actual_gamestate == expected_gamestate:
        if actual_positions == expected_positions:
            return True

    if actual_gamestate != expected_gamestate:
        print("act gamestate", actual_gamestate)
        print("exp gamestate", expected_gamestate)
        print(difference_between_dictionaries(actual_gamestate, expected_gamestate))

    if actual_positions != expected_positions:
        print("act position", actual_positions)
        print("exp position", expected_positions)

    return False


def read_positions(positions):
    for key, value in positions.items():
        if value == "None":
            value = None
        else:
            value = Position.from_string(value)
        positions[key] = value
    return positions


def pick_upgrade(choice, unit):
    return unit.get_upgrade(choice)


def is_outcome_correct(test_document):
    game = Game.from_log_document(test_document)
    controller = Controller(View(), Sound())
    controller.positions = read_positions(test_document["pre_positions"])

    controller.game = game
    click_position = Position.from_string(test_document["click_position"])

    if "outcome" in test_document:
        outcome = Outcome.from_document(test_document["outcome"])
        controller.determine_outcome = partial(determine_outcome, outcome)

    if "end_at" in test_document:
        end_at = test_document["end_at"]
        controller.pick_end_at = partial(pick_end_at, end_at)

    if "upgrade_choice" in test_document:
        upgrade_choice = int(test_document["upgrade_choice"])
        controller.pick_upgrade = partial(pick_upgrade, upgrade_choice)

    if "move_with_attack" in test_document:
        controller.ask_about_move_with_attack = partial(ask_about_move_with_attack, test_document["move_with_attack"])

    controller.game.gamestate.set_available_actions()

    controller.game.save = save

    controller.add_log = add_log

    controller.left_click(click_position)

    actual_gamestate = controller.game.gamestate.to_document()
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"]).to_document()

    actual_positions = controller.positions
    expected_positions = read_positions(test_document["post_positions"])

    return give_output(actual_gamestate, expected_gamestate, actual_positions, expected_positions)


def is_outcome_correct_extra_action(test_document):
    gamestate = Gamestate.from_document(test_document["pre_gamestate"])
    expected_gamestate = Gamestate.from_document(test_document["post_gamestate"])

    action = Action.from_document(gamestate.all_units(), test_document["action"])
    outcome = Outcome.from_document(test_document["outcome1"]) if "outcome1" in test_document else None
    gamestate.do_action(action, outcome)

    extra_action = Action.from_document(gamestate.all_units(), test_document["extra_action"])
    outcome = Outcome.from_document(test_document["outcome2"]) if "outcome2" in test_document else None
    gamestate.do_action(extra_action, outcome)

    actual = gamestate.to_document()
    expected = expected_gamestate.to_document()
    return actual == expected


def utest(test_document):
    return globals()[test_document["type"].lower().replace(" ", "_").replace(",", "")](test_document)


def run():

    testcase_files = glob.glob("./tests/test_files/*.json")
    #testcase_files = ["./tests/test_files\Fencer_attack2.json"] #running just 1 test.

    run_method(testcase_files, utest)

