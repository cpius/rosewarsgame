from __future__ import division
from common import *
from action import Action


def do_action(gamestate, action, outcome):
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

    unit = action.unit

    apply_unit_effects()

    update_actions_remaining()

    update_unit_position()

    attack_direction = None
    if action.is_attack() and action.unit.is_melee():
        attack_direction = action.end_at.get_direction_to(action.target_at)

    if action.is_push():
        settle_attack_push(action, gamestate, outcome)

        if action.is_triple_attack():
            for forward_position in action.end_at.two_forward_tiles(attack_direction):
                if forward_position in gamestate.enemy_units:
                    sub_action = Action(
                        gamestate.all_units(),
                        action.start_at,
                        end_at=action.end_at,
                        target_at=forward_position)
                    do_sub_action(gamestate, sub_action, attack_direction, outcome)

    elif action.is_attack():
        settle_attack(action, gamestate, outcome)

        if action.unit.has(Trait.longsword):
            for forward_position in action.end_at.four_forward_tiles(attack_direction):
                if forward_position in gamestate.enemy_units:
                    sub_action = Action(
                        gamestate.all_units(),
                        action.start_at,
                        end_at=action.end_at,
                        target_at=forward_position)

                    settle_attack(sub_action, gamestate, outcome)

    elif action.is_ability():
        settle_ability(action, gamestate.enemy_units, gamestate.player_units)

    if unit.has(Trait.bloodlust) and action.is_successful(outcome.outcomes[action.target_at], gamestate):
        bloodlust = True
    else:
        unit.remove(Trait.extra_action)
        bloodlust = False

    if gamestate.extra_action and not bloodlust:
        unit.set(Trait.movement_remaining, 0)
    else:
        prepare_extra_actions(action, unit)

    update_unit_to_final_position(gamestate, action)

    gamestate.extra_action = unit.has(Trait.extra_action)


def settle_attack_push(action, gamestate, outcome, push_direction=None):
    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units

    rolls = outcome.for_position(action.target_at)

    if not push_direction:
        push_direction = action.end_at.get_direction_to(action.target_at)

    push_destination = push_direction.move(action.target_at)

    if action.is_miss(rolls, gamestate):
        return

    if action.is_successful(rolls, gamestate):
        action.unit.gain_xp()

        if action.target_unit.has_extra_life():
            action.target_unit.set(Trait.lost_extra_life)

            if not push_destination.out_of_board_vertical():
                update_final_position(action)
                destination_is_occupied = push_destination in player_units or push_destination in enemy_units
                if destination_is_occupied or push_destination.out_of_board_horizontal():
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


def do_sub_action(gamestate, action, direction, outcome):
    if action.is_triple_attack():
        settle_attack_push(action, gamestate, outcome, direction)


def settle_attack(action, gamestate, outcome):
    rolls = outcome.for_position(action.target_at)

    if action.is_failure(rolls, gamestate):
        return

    if action.target_unit.has_extra_life():
        action.target_unit.set(Trait.lost_extra_life)
    else:
        del gamestate.enemy_units[action.target_at]

        if action.is_successful(rolls, gamestate):
            update_final_position(action)


def settle_ability(action, enemy_units, player_units):
    if action.ability == Ability.bribe:
        action.target_unit.set(Trait.bribed)
        player_units[action.target_at] = enemy_units.pop(action.target_at)
    else:
        action.target_unit.do(action.ability)


def update_final_position(action):
    if action.move_with_attack and action.unit.is_melee():
        action.final_position = action.target_at


def update_unit_to_final_position(gamestate, action):
    gamestate.player_units[action.final_position] = gamestate.player_units.pop(action.end_at)
