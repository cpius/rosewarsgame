from __future__ import division
import random as rnd
import battle
from common import *
from outcome import Outcome
from action import Action


def do_action(gamestate, action, outcome=None):
    def prepare_extra_actions(action, unit):
        if unit.has(Trait.swiftness):
            movement_remaining = unit.movement - distance(action.start_at, action.end_at) - int(action.is_attack())
            unit.set(Trait.movement_remaining, movement_remaining)
            unit.set(Trait.extra_action)

        if unit.has(Trait.combat_agility):
            unit.set(Trait.movement_remaining, unit.movement - distance(action.start_at, action.final_position))
            unit.set(Trait.extra_action)

    def update_actions_remaining():

        if gamestate.extra_action:
            return

        gamestate.decrement_actions_remaining()

        if action.double_cost():
            gamestate.decrement_actions_remaining()

    def apply_unit_effects():
        if unit.has(Trait.attack_cooldown) and action.is_attack():
            unit.set(Trait.attack_frozen, 3)

        if unit.has(Trait.attack_cooldown_II) and action.is_attack():
            unit.set(Trait.attack_frozen, 2)

        unit.gain_xp()
        unit.set(Trait.used)

    def update_unit_position():
        gamestate.player_units[action.end_at] = gamestate.player_units.pop(action.start_at)

    def update_unit_to_final_position():
        gamestate.player_units[action.final_position] = gamestate.player_units.pop(action.end_at)

    if not outcome:
        outcome = Outcome()

    unit = action.unit

    apply_unit_effects()

    update_actions_remaining()

    update_unit_position()

    end_at = action.end_at
    target_at = action.target_at

    if action.is_attack() and action.unit.is_melee():
        attack_direction = end_at.get_direction_to(target_at)

    if action.is_push():
        outcome = settle_attack_push(action, gamestate, outcome)

        if action.is_triple_attack():
            for forward_position in action.end_at.two_forward_tiles(attack_direction):
                if forward_position in gamestate.enemy_units:
                    sub_action = Action(
                        gamestate.all_units(),
                        action.start_at,
                        end_at=end_at,
                        target_at=forward_position)
                    sub_action.unit = action.unit
                    sub_action.target_unit = gamestate.enemy_units[forward_position]
                    outcome = do_sub_action(gamestate, sub_action, attack_direction, outcome)

    elif action.is_attack():
        outcome = settle_attack(action, gamestate, outcome)

        if action.unit.has(Trait.longsword):
            direction = end_at.get_direction_to(target_at)

            for forward_position in end_at.four_forward_tiles(direction):
                if forward_position in gamestate.enemy_units:
                    sub_action = Action(
                        gamestate.all_units(),
                        action.start_at,
                        end_at=end_at,
                        target_at=forward_position)

                    outcome = settle_attack(sub_action, gamestate, outcome)

    elif action.is_ability():
        settle_ability(action, gamestate.enemy_units, gamestate.player_units)

    if unit.has(Trait.bloodlust) and outcome.outcomes[action.target_at] == SubOutcome.WIN:
        bloodlust = True
    else:
        unit.remove(Trait.extra_action)
        bloodlust = False

    if gamestate.extra_action and not bloodlust:
        unit.set(Trait.movement_remaining, 0)
    else:
        prepare_extra_actions(action, unit)

    update_unit_to_final_position()

    gamestate.extra_action = unit.has(Trait.extra_action)

    return outcome


def settle_attack_push(action, gamestate, outcome=None, push_direction=None):
    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    if not outcome:
        outcome = Outcome()

    sub_outcome = outcome.for_position(action.target_at)

    if Outcome.is_failure(sub_outcome):
        return outcome

    if sub_outcome == SubOutcome.UNKNOWN:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        if not battle.attack_successful(action, rolls, gamestate):
            outcome.set_suboutcome(action.target_at, SubOutcome.MISS)
            return

        defense_successful = battle.defence_successful(action, rolls, gamestate)
        if defense_successful:
            outcome.set_suboutcome(action.target_at, SubOutcome.PUSH)
        else:
            outcome.set_suboutcome(action.target_at, SubOutcome.WIN)

    if not push_direction:
        push_direction = action.end_at.get_direction_to(action.target_at)

    push_destination = push_direction.move(action.target_at)

    if outcome.for_position(action.target_at) == SubOutcome.WIN:
        action.unit.gain_xp()

        if action.target_unit.has(Trait.extra_life)  and not action.target_unit.has(Trait.lost_extra_life):
            action.target_unit.set(Trait.lost_extra_life)

            if not push_destination.out_of_board_vertical():
                update_final_position(action)
                if push_destination in player_units or push_destination in enemy_units or push_destination.out_of_board_horizontal():
                    del enemy_units[action.target_at]
                else:
                    enemy_units[push_destination] = enemy_units.pop(action.target_at)

        else:
            update_final_position(action)
            del enemy_units[action.target_at]

    else:
        if not push_destination.out_of_board_vertical():
            update_final_position(action)

            is_push_destination_occupied = push_destination in player_units or push_destination in enemy_units

            if is_push_destination_occupied or push_destination.out_of_board_horizontal():
                del enemy_units[action.target_at]
            else:
                enemy_units[push_destination] = enemy_units.pop(action.target_at)

    return outcome


def do_sub_action(gamestate, action, direction, outcome):
    if action.is_triple_attack():
        return settle_attack_push(action, gamestate, outcome, direction)


def settle_attack(action, gamestate, outcome):
    if not outcome:
        outcome = Outcome()

    sub_outcome = outcome.for_position(action.target_at)

    if Outcome.is_failure(sub_outcome):
        return outcome

    if sub_outcome == SubOutcome.UNKNOWN:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]

        attack_successful = battle.attack_successful(action, rolls, gamestate)
        defence_successful = battle.defence_successful(action, rolls, gamestate)
        if not attack_successful or defence_successful:
            if not attack_successful:
                outcome.set_suboutcome(action.target_at, SubOutcome.MISS)
            else:
                outcome.set_suboutcome(action.target_at, SubOutcome.DEFEND)
            return outcome

    outcome.set_suboutcome(action.target_at, SubOutcome.WIN)

    if action.target_unit.has(Trait.extra_life) and not action.target_unit.has(Trait.lost_extra_life):
        action.target_unit.set(Trait.lost_extra_life)
    else:
        del gamestate.enemy_units[action.target_at]

        if outcome.for_position(action.target_at) == SubOutcome.WIN:
            update_final_position(action)

    return outcome


def settle_ability(action, enemy_units, player_units):
    if action.ability == Ability.bribe:
        action.target_unit.set(Trait.bribed)
        player_units[action.target_at] = enemy_units.pop(action.target_at)
    else:
        action.target_unit.do(action.ability)


def update_final_position(action):
    if action.is_move_with_attack() and action.unit.is_melee():
        action.final_position = action.target_at


