from __future__ import division
from common import *
from action import Action


def do_action(gamestate, action, outcome):

    def settle_attack(action):
        rolls = outcome.for_position(action.target_at)

        if not action.is_win(rolls, gamestate):
            return

        if action.target_unit.has_extra_life():
            action.target_unit.set(State.lost_extra_life)
        else:
            del enemy_units[action.target_at]

    def settle_ability(action):
        if action.ability == Ability.bribe:
            action.target_unit.set(Effect.bribed)
            player_units[action.target_at] = enemy_units.pop(action.target_at)
        else:
            value = action.unit.abilities[action.ability]
            action.target_unit.do(action.ability, value)

    def prepare_extra_actions(action):
        if action.unit.has(State.extra_action):
            unit.remove(State.extra_action)

            if unit.has(Trait.bloodlust) and action.is_attack() and action.is_win(rolls, gamestate):
                unit.set(State.movement_remaining, unit.get(State.movement_remaining) - int(action.move_with_attack))
                unit.set(State.extra_action)
            else:
                unit.remove(State.movement_remaining)

        elif action.is_attack():
            movement_remaining = unit.movement - distance(action.start_at, action.target_at)

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

    def update_unit_position():
        player_units[action.end_at] = player_units.pop(action.start_at)

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

    if action.is_attack():
        unit.gain_xp()
        rolls = outcome.for_position(action.target_at)
        settle_attack(action)

        if unit.has(Trait.triple_attack):
            triple_attack()
        elif unit.has(Trait.longsword):
            longsword()

    elif action.is_ability():
        unit.gain_xp()
        settle_ability(action)

    if any(unit.has(trait) for trait in [Trait.swiftness, Trait.combat_agility, Trait.bloodlust]):
        prepare_extra_actions(action)

    if action.is_attack() and action.move_with_attack and action.attack_successful(rolls, gamestate):
        move_melee_unit_to_target_tile(gamestate, rolls, action)

    unit.set(State.used)


def move_melee_unit_to_target_tile(gamestate, rolls, action):

    if action.is_win(rolls, gamestate):
        if not action.target_unit.has_extra_life():
            gamestate.player_units[action.target_at] = gamestate.player_units.pop(action.end_at)

    elif action.is_push() and action.attack_successful(rolls, gamestate):
        attack_direction = action.end_at.get_direction_to(action.target_at)
        push_destination = attack_direction.move(action.target_at)
        enemy_units = gamestate.enemy_units

        if not push_destination.out_of_board_vertical():
            if push_destination in gamestate.all_units() or push_destination.out_of_board_horizontal():
                del enemy_units[action.target_at]
            else:
                enemy_units[push_destination] = enemy_units.pop(action.target_at)

            gamestate.player_units[action.target_at] = gamestate.player_units.pop(action.end_at)
