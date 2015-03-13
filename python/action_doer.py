from __future__ import division
from common import *
from action import Action
import battle


def do_action(gamestate, action, outcome):

    def settle_attack(action, attack_direction=None, is_sub_action=False):
        rolls = outcome.for_position(action.target_at)

        if battle.is_win(action, rolls, gamestate, is_sub_action):
            if action.target_unit.has_extra_life():
                action.target_unit.set(State.lost_extra_life)
            else:
                del enemy_units[action.target_at]

        elif action.is_push() and battle.attack_successful(action, rolls, gamestate):
            if not attack_direction:
                attack_direction = action.end_at.get_direction_to(action.target_at)
            push_destination = attack_direction.move(action.target_at)

            if push_destination in all_units or push_destination not in board:
                del enemy_units[action.target_at]
            else:
                enemy_units[push_destination] = enemy_units.pop(action.target_at)

        if battle.flanking(action) and action.target_at in enemy_units:
            action.target_unit.set(State.flanked)

    def settle_ability(action):
        if action.ability == Ability.bribe:
            action.target_unit.set(Effect.bribed, duration=1)
            player_units[action.target_at] = enemy_units.pop(action.target_at)
        elif action.ability == Ability.assassinate:
            if outcome.outcomes[action.target_at].attack > 2:
                del enemy_units[action.target_at]
            if outcome.outcomes[action.target_at].defence > 2:
                del player_units[action.start_at]
        else:
            level = action.unit.get_level(action.ability)
            action.target_unit.do(action.ability, level)

    def prepare_extra_actions(action):
        if action.unit.has(State.extra_action):
            unit.remove(State.extra_action)
            unit.remove(State.movement_remaining)

        elif action.is_attack():
            movement_remaining = unit.movement - distance(action.start_at, action.end_at) - 1

            if unit.has(Trait.combat_agility) and action.is_attack() and not battle.is_win(action, rolls, gamestate):
                movement_remaining += 1

            if movement_remaining:
                unit.set(State.movement_remaining, movement_remaining)

            if movement_remaining or unit.has(Trait.combat_agility):
                unit.set(State.extra_action)

    def update_actions_remaining():

        if unit.has(State.extra_action):
            return

        gamestate.decrement_actions_remaining()

        if action.double_cost():
            gamestate.decrement_actions_remaining()

    def apply_unit_effects():
        if unit.has(Trait.attack_cooldown) and action.is_attack():
            unit.set(Effect.attack_frozen, duration=3)

        if unit.has(Trait.attack_cooldown, 2) and action.is_attack():
            unit.set(Effect.attack_frozen, level=2, duration=2)

    def update_unit_position():
        player_units[action.end_at] = player_units.pop(action.start_at)

    def triple_attack():
        for position in action.end_at.two_forward_tiles(attack_direction) & set(enemy_units):
            sub_action = Action(all_units, action.start_at, action.end_at, target_at=position)
            settle_attack(sub_action, attack_direction, True)

    def spread_attack():
        for position in action.target_at.adjacent_tiles() & set(enemy_units):
            sub_action = Action(all_units, action.start_at, action.end_at, target_at=position)
            settle_attack(sub_action, None, True)

    def longsword():
        for position in action.end_at.four_forward_tiles(attack_direction) & set(enemy_units):
            sub_action = Action(all_units, action.start_at, action.end_at, target_at=position)
            settle_attack(sub_action, None, True)

    unit = action.unit
    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    all_units = gamestate.all_units()

    apply_unit_effects()

    update_actions_remaining()

    update_unit_position()

    if action.is_attack() or unit.type == Type.Cavalry or action.is_ability():
        unit.gain_experience()

    if action.is_attack():
        if action.unit.is_melee() and not action.is_javelin_throw():
            attack_direction = action.end_at.get_direction_to(action.target_at)
        rolls = outcome.for_position(action.target_at)
        settle_attack(action)

        if unit.has(Trait.triple_attack):
            triple_attack()
        elif unit.has(Trait.longsword):
            longsword()
        elif unit.has(Trait.spread_attack):
            spread_attack()

        if action.is_javelin_throw():
            unit.set(State.javelin_thrown)

        if action.move_with_attack and battle.attack_successful(action, rolls, gamestate):
            move_melee_unit_to_target_tile(gamestate, rolls, action)

    elif action.is_ability():
        settle_ability(action)

    if any(unit.has(attribute) for attribute in [Trait.swiftness, Trait.combat_agility]):
        prepare_extra_actions(action)

    unit.set(State.used, value=1)


def move_melee_unit_to_target_tile(gamestate, rolls, action):

    if battle.is_win(action, rolls, gamestate) and not action.target_unit.has_extra_life():
        gamestate.player_units[action.target_at] = gamestate.player_units.pop(action.end_at)

    elif action.is_push() and battle.attack_successful(action, rolls, gamestate):
        gamestate.player_units[action.target_at] = gamestate.player_units.pop(action.end_at)
