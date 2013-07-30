from __future__ import division
import random as rnd
import battle
from common import *
from outcome import Outcome
import settings
from action import Action


def do_action(gamestate, action, outcome=None):
    def prepare_extra_actions(action, unit):

        if unit.has("swiftness"):
            movement_remaining = unit.movement - distance(action.start_position, action.end_position)
            if action.is_attack():
                movement_remaining -= 1
            unit.set_movement_remaining(movement_remaining)
            unit.set("extra_action")

        if unit.has("combat_agility"):
            unit.set_movement_remaining(unit.movement - distance(action.start_position, action.final_position))
            unit.set("extra_action")

    def update_actions_remaining(action):

        if gamestate.extra_action:
            return

        gamestate.decrement_actions_remaining()

        if action.double_cost:
            gamestate.decrement_actions_remaining()

    def secondary_action_effects(action, unit):
        if unit.has("attack_cooldown") and action.is_attack():
            unit.set_attack_frozen(unit.attack_cooldown)

        if action.unit.has("double_attack_cost") and action.is_attack():
            action.double_cost = True

    if not outcome:
        outcome = Outcome()

    action.add_references(gamestate)
    unit = action.unit

    secondary_action_effects(action, unit)

    update_actions_remaining(action)

    unit.gain_xp()
    unit.set("used")

    if action.start_position in gamestate.player_units():
        gamestate.player_units()[action.end_position] = gamestate.player_units().pop(action.start_position)

    end_position = action.end_position
    attack_position = action.attack_position
    if action.is_attack() and action.unit.range == 1:
        attack_direction = end_position.get_direction(attack_position)

    if action.is_push():
        outcome = settle_attack_push(action, gamestate, outcome)

        if action.is_triple_attack():
            for forward_position in action.end_position.two_forward_tiles(attack_direction):
                if forward_position in gamestate.opponent_units():
                    sub_action = Action(
                        action.start_position,
                        end_position=end_position,
                        attack_position=forward_position)
                    sub_action.unit = action.unit
                    sub_action.target_unit = gamestate.opponent_units()[forward_position]
                    outcome = do_sub_action(gamestate, sub_action, attack_direction, outcome)

    elif action.is_attack():
        outcome = settle_attack(action, gamestate, outcome)
    elif action.is_ability():
        settle_ability(action, gamestate.opponent_units(), gamestate.player_units())

    if unit.has("bloodlust") and outcome.outcomes[action.attack_position] == 1:
        bloodlust = True
    else:
        unit.remove("extra_action")
        bloodlust = False

    if gamestate.extra_action and not bloodlust:
        gamestate.extra_action = 0
        unit.set_movement_remaining(0)
    else:
        prepare_extra_actions(action, unit)

    if action.end_position in gamestate.player_units():
        gamestate.player_units()[action.final_position] = gamestate.player_units().pop(action.end_position)

    if gamestate.extra_action:
        gamestate.extra_action = False

    if unit.has("extra_action"):
        gamestate.extra_action = True

    return outcome


def settle_attack_push(action, gamestate, outcome=None, push_direction=None):
    player_units = gamestate.player_units()
    opponent_units = gamestate.opponent_units()
    if not outcome:
        outcome = Outcome()

    sub_outcome = outcome.for_position(action.attack_position)

    if Outcome.is_failure(sub_outcome):
        return outcome

    if sub_outcome == SubOutcome.UNKNOWN:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        if not battle.attack_successful(action, rolls, gamestate):
            outcome.set_suboutcome(action.attack_position, SubOutcome.MISS)
            return

        defense_successful = battle.defence_successful(action, rolls, gamestate)
        if defense_successful:
            outcome.set_suboutcome(action.attack_position, SubOutcome.PUSH)
        else:
            outcome.set_suboutcome(action.attack_position, SubOutcome.WIN)

    if not push_direction:
        push_direction = action.end_position.get_direction(action.attack_position)

    push_destination = push_direction.move(action.attack_position)

    if outcome.for_position(action.attack_position) == SubOutcome.WIN:
        action.unit.gain_xp()

        if action.target_unit.has("extra_life"):
            action.target_unit.remove("extra_life")

            if not push_destination.out_of_board_vertical():
                update_final_position(action)
                if push_destination in player_units or push_destination in opponent_units or push_destination.out_of_board_horizontal():
                    del opponent_units[action.attack_position]
                else:
                    opponent_units[push_destination] = opponent_units.pop(action.attack_position)

        else:
            update_final_position(action)
            del opponent_units[action.attack_position]

    else:
        if not push_destination.out_of_board_vertical():
            update_final_position(action)

            is_push_destination_occupied = push_destination in player_units or push_destination in opponent_units

            if is_push_destination_occupied or push_destination.out_of_board_horizontal():
                del opponent_units[action.attack_position]
            else:
                opponent_units[push_destination] = opponent_units.pop(action.attack_position)

    return outcome


def do_sub_action(gamestate, action, direction, outcome):
    if action.is_triple_attack():
        return settle_attack_push(action, gamestate, outcome, direction)


def settle_attack(action, gamestate, outcome):
    if not outcome:
        outcome = Outcome()

    sub_outcome = outcome.for_position(action.attack_position)

    if Outcome.is_failure(sub_outcome):
        return outcome

    if sub_outcome == SubOutcome.UNKNOWN:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]

        attack_successful = battle.attack_successful(action, rolls, gamestate)
        defence_successful = battle.defence_successful(action, rolls, gamestate)
        if not attack_successful or defence_successful:
            if not attack_successful:
                outcome.set_suboutcome(action.attack_position, SubOutcome.MISS)
            else:
                outcome.set_suboutcome(action.attack_position, SubOutcome.DEFEND)
            return outcome

    outcome.set_suboutcome(action.attack_position, SubOutcome.WIN)

    if action.target_unit.has("extra_life"):
        action.target_unit.remove("extra_life")
    else:
        del gamestate.opponent_units()[action.attack_position]

        if outcome.for_position(action.attack_position) == SubOutcome.WIN:
            update_final_position(action)

    return outcome


def settle_ability(action, enemy_units, player_units):

    if action.ability == "bribe":
        action.target_unit.set_bribed()
        player_units[action.ability_position] = enemy_units.pop(action.ability_position)
        player_units[action.ability_position].set_bribed()

    else:
        print action.ability
        action.target_unit.set(action.ability)


def update_final_position(action):
    if action.is_move_with_attack() and action.unit.range == 1:
        action.final_position = action.attack_position


