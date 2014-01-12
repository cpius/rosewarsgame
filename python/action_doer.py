from __future__ import division
from common import *
from action import Action


def apply_push(action, push_destination, enemy_units, all_units):
    if not push_destination.out_of_board_vertical():
        if push_destination in all_units or push_destination.out_of_board_horizontal():
            del enemy_units[action.target_at]
        else:
            enemy_units[push_destination] = enemy_units.pop(action.target_at)


def do_action(gamestate, action, outcome):

    def settle_attack(action):
        rolls = outcome.for_position(action.target_at)

        if action.is_failure(rolls, gamestate):
            return

        if action.target_unit.has_extra_life():
            action.target_unit.set(State.lost_extra_life)
        else:
            del enemy_units[action.target_at]

    def settle_ability(action):
        if action.ability == Ability.bribe:
            action.target_unit.set(State.bribed)
            player_units[action.target_at] = enemy_units.pop(action.target_at)
        else:
            value = action.unit.abilities[action.ability]
            action.target_unit.do(action.ability, value)

    def prepare_extra_actions(action):
        if action.unit.has(State.extra_action):
            unit.remove(State.extra_action)

            if unit.has(Trait.bloodlust) and action.is_attack() and action.is_successful(rolls, gamestate):
                unit.set(State.movement_remaining, unit.get(State.movement_remaining) - int(action.move_with_attack))
                unit.set(State.extra_action)
            else:
                unit.remove(State.movement_remaining)

        elif action.is_attack():
            movement_remaining = unit.movement - distance(action.start_at, action.target_at)

            #if unit.has(Trait.combat_agility) and action.is_attack() and action.is_successful(rolls, gamestate):
            #    movement_remaining -= 1

            unit.set(State.movement_remaining, movement_remaining)

            if movement_remaining:
                unit.set(State.extra_action)
            elif unit.has(Trait.combat_agility):
                unit.set(State.extra_action)

    def update_actions_remaining():

        if unit.has(State.extra_action):
            return

        gamestate.decrement_actions_remaining()

        if action.double_cost():
            gamestate.decrement_actions_remaining()

    def apply_unit_effects():
        if unit.has(Trait.attack_cooldown) and action.is_attack():
            unit.set(State.attack_frozen, 3)

        if unit.has(Trait.attack_cooldown, 2) and action.is_attack():
            unit.set(State.attack_frozen, 2)

        unit.gain_xp()
        unit.set(State.used)

    def update_unit_position():
        player_units[action.end_at] = player_units.pop(action.start_at)
        action.unit.place(action.end_at)

    def triple_attack():
        for position in action.end_at.two_forward_tiles(attack_direction):
            if position in enemy_units:
                sub_action = Action(all_units, action.start_at, action.end_at, position)
                settle_attack(sub_action)

    def longsword():
        for position in action.end_at.four_forward_tiles(attack_direction):
            if position in enemy_units:
                sub_action = Action(all_units, action.start_at, action.end_at, position)
                settle_attack(sub_action)

    unit = action.unit
    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    all_units = gamestate.all_units()
    if action.is_attack() and action.unit.is_melee():
        attack_direction = action.end_at.get_direction_to(action.target_at)

    apply_unit_effects()

    update_actions_remaining()

    update_unit_position()
    rolls = outcome.for_position(action.target_at)

    if action.is_attack():

        settle_attack(action)

        for trait in [Trait.triple_attack, Trait.longsword]:
            if unit.has(trait):
                locals()[Trait.name[trait]]()

    elif action.is_ability():
        settle_ability(action)

    if any(unit.has(trait) for trait in [Trait.swiftness, Trait.combat_agility, Trait.bloodlust]):
        prepare_extra_actions(action)

    if action.is_attack() and action.move_with_attack and action.attack_successful(rolls, gamestate):
        move_melee_unit_to_target_tile(gamestate, action)


def move_melee_unit_to_target_tile(gamestate, action):
    gamestate.player_units[action.target_at] = gamestate.player_units.pop(action.end_at)
    action.unit.place(action.target_at)
    attack_direction = action.end_at.get_direction_to(action.target_at)
    push_destination = attack_direction.move(action.target_at)

    print "A"
    if action.is_push():
        print "B"
        apply_push(action, push_destination, gamestate.enemy_units, gamestate.all_units)
