from __future__ import division
from common import *
from action import Action


def do_action(gamestate, action, outcome):

    def settle_attack_push(action):

        def apply_push():
            if not push_destination.out_of_board_vertical():
                update_final_position(action)
                if push_destination in all_units or push_destination.out_of_board_horizontal():
                    del enemy_units[action.target_at]
                else:
                    enemy_units[push_destination] = enemy_units.pop(action.target_at)

        rolls = outcome.for_position(action.target_at)
        push_destination = attack_direction.move(action.target_at)

        if action.is_miss(rolls, gamestate):
            return

        if action.is_successful(rolls, gamestate):
            if action.target_unit.has_extra_life():
                action.target_unit.set(Trait.lost_extra_life)
                apply_push()
            else:
                update_final_position(action)
                del enemy_units[action.target_at]
        else:
            apply_push()

    def settle_attack(action):
        rolls = outcome.for_position(action.target_at)

        if action.is_failure(rolls, gamestate):
            return

        if action.target_unit.has_extra_life():
            action.target_unit.set(Trait.lost_extra_life)
        else:
            del enemy_units[action.target_at]
            update_final_position(action)

    def do_sub_action(action):
        if action.is_push():
            settle_attack_push(action)
        else:
            settle_attack(action)

    def settle_ability(action):
        if action.ability == Ability.bribe:
            action.target_unit.set(Trait.bribed)
            player_units[action.target_at] = enemy_units.pop(action.target_at)
        else:
            action.target_unit.do(action.ability)

    def prepare_extra_actions(action):

        if unit.has(Trait.swiftness):
            movement_remaining = unit.movement - distance(action.start_at, action.end_at) - int(action.is_attack())
            unit.set(Trait.movement_remaining, movement_remaining)
            unit.set(Trait.extra_action)

        if unit.has(Trait.combat_agility) and not gamestate.extra_action:
            movement_remaining = unit.movement - distance(action.start_at, action.final_position)
            unit.set(Trait.movement_remaining, movement_remaining)
            unit.set(Trait.extra_action)

        if unit.has(Trait.bloodlust) and action.is_attack() and action.is_successful(rolls, gamestate):
            movement_remaining = unit.get(Trait.movement_remaining) - distance(action.start_at, action.final_position)
            unit.set(Trait.movement_remaining, movement_remaining)
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
        player_units[action.end_at] = player_units.pop(action.start_at)

    def triple_attack():
        for forward_position in action.end_at.two_forward_tiles(attack_direction):
            if forward_position in enemy_units:
                sub_action = Action(all_units, action.start_at, action.end_at, forward_position)
                do_sub_action(sub_action)

    def longsword():
        for forward_position in action.end_at.four_forward_tiles(attack_direction):
            if forward_position in enemy_units:
                sub_action = Action(all_units, action.start_at, action.end_at, forward_position)
                do_sub_action(sub_action)

    unit = action.unit
    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    all_units = gamestate.all_units()
    attack_direction = None
    if action.is_attack() and action.unit.is_melee():
        attack_direction = action.end_at.get_direction_to(action.target_at)

    apply_unit_effects()

    update_actions_remaining()

    unit.remove(Trait.extra_action)

    update_unit_position()

    if action.is_attack():
        rolls = outcome.for_position(action.target_at)
        if action.is_push():
            settle_attack_push(action)
        else:
            settle_attack(action)

        for trait in [Trait.triple_attack, Trait.longsword]:
            if unit.has(trait):
                locals()[Trait.reverse_mapping[trait]]()

    elif action.is_ability():
        settle_ability(action)

    prepare_extra_actions(action)

    update_unit_to_final_position(gamestate, action)

    gamestate.extra_action = unit.has(Trait.extra_action)


def update_final_position(action):
    if action.move_with_attack and action.unit.is_melee():
        action.final_position = action.target_at


def update_unit_to_final_position(gamestate, action):
    gamestate.player_units[action.final_position] = gamestate.player_units.pop(action.end_at)
