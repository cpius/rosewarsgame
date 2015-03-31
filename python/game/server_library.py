from gamestate.gamestate_library import *
from gamestate.action import Action
from gamestate.outcome import Outcome
from game.game_library import document_to_string


def validate_upgrade(action_document, gamestate):
    position, unit = gamestate.get_upgradeable_unit()
    upgrade_options = [unit.get_upgrade(0), unit.get_upgrade(1)]
    upgrade = get_enum_attributes(action_document["upgrade"])

    if upgrade in upgrade_options:
        message = "Upgraded " + unit.pretty_name + " on " + str(position)
        new_unit = unit.get_upgraded_unit_from_upgrade(upgrade)
        new_unit_string = document_to_string(new_unit.to_document())

        return True, message, new_unit_string
    else:
        option1 = str(get_string_attributes(upgrade_options[0]))
        option2 = str(get_string_attributes(upgrade_options[1]))
        message = "The upgrade must be one of " + option1 + " or " + option2

        return False, message, ""


def validate_action(gamestate, action_document):

    gamestate.set_available_actions()
    available_actions = gamestate.get_actions_including_move_with_attack_none()

    if Position.from_string(action_document["start_at"]) not in gamestate.player_units:
        return invalid_action(available_actions, request.json)

    action = Action.from_document(gamestate.all_units(), action_document)

    if not action:
        return invalid_action(available_actions, request.json)

    if not action in available_actions:
        return invalid_action(available_actions, str(action))

    return action


def invalid_action(available_actions, requested_action):
    return {
        "Status": "Error",
        "Message": "Invalid action",
        "Action": requested_action,
        "Available actions": ", ".join(str(action) for action in available_actions)
    }


def determine_outcome_if_any(action, gamestate):
    outcome = None

    if action.has_outcome:
        outcome = Outcome.determine_outcome(action, gamestate)

    return outcome
