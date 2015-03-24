from action import Action
from common import *
import action_sets


def get_actions(gamestate):

    is_extra_action = gamestate.is_extra_action()

    if not gamestate.actions_remaining and not is_extra_action:
        return []

    actions = []
    for position, unit in gamestate.player_units.items():
        if can_use_unit(unit, is_extra_action):
            actions += get_unit_actions(unit, position, gamestate)

    return actions


def get_unit_actions(unit, start_at, gamestate):

    def melee_attack_actions(moveset):
        return [make_action(**terms) for terms in attack_generator(moveset)]

    def ranged_attack_actions(attackset):
        return [make_action(end_at=start_at, target_at=target_at) for target_at in attackset]

    def make_ability_actions(abilityset, ability):
        return [make_action(end_at=start_at, target_at=position, ability=ability) for position in abilityset]

    def make_move_actions(moveset):
        return [make_action(end_at) for end_at in moveset]

    def generate_movesets(movement):
        return action_sets.moves_sets(start_at, frozenset(units), zoc_blocks, movement, movement)

    def generate_moveset(movement):
        return action_sets.moves_set(start_at, frozenset(units), zoc_blocks, movement, movement)

    def generate_extra_moveset():
        movement = unit.get_state(State.movement_remaining)
        return action_sets.moves_set(start_at, frozenset(units), zoc_blocks, movement, movement)

    def get_defence_maneuverability_actions():

        moveset_with_leftover, moveset_no_leftover = generate_movesets(2)
        moveset = moveset_with_leftover | moveset_no_leftover
        attacks = melee_attack_actions(moveset_with_leftover | {start_at})
        moves = make_move_actions(moveset)

        moves = [move for move in moves if abs(move.start_at.row - move.end_at.row) < 2]
        attacks = [attack for attack in attacks if abs(attack.start_at.row - attack.target_at.row) < 2]

        return moves, attacks

    def get_javelin_attacks():
        javelin_attacks = ranged_attack_actions(get_ranged_attack_tiles(3))
        javelin_attacks = [attack for attack in javelin_attacks if distance(attack.end_at, attack.target_at) > 1]
        return javelin_attacks

    def get_rage_attacks():
        moveset = generate_moveset(unit.movement)
        return [make_action(move_with_attack=False, **terms) for terms in attack_generator_no_zoc_check(moveset)]

    def get_extra_actions():

        def get_actions_combat_agility():
            for terms in attack_generator({start_at}):
                if terms["move_with_attack"]:
                    if unit.get_state(State.movement_remaining):
                        attacks.append(Action(units, start_at, **terms))
                else:
                    attacks.append(Action(units, start_at, **terms))
            return attacks

        moveset = generate_extra_moveset()
        moves = make_move_actions(moveset)

        attacks = []

        if unit.has(Trait.combat_agility):
            attacks = get_actions_combat_agility()
            moves = []

        if moves or attacks:
            moves.append(Action(units, start_at, end_at=start_at))  # Add an action for indicating pass on the extra action

        return moves, attacks

    def get_ride_through_attacks():
        ride_through_attacks = []
        for direction, one_tile_away in start_at.adjacent_moves().items():
            two_tiles_away = one_tile_away.move(direction)
            if one_tile_away in enemy_units and two_tiles_away and two_tiles_away not in units:
                attack = make_action(end_at=two_tiles_away, target_at=one_tile_away, move_with_attack=False)
                ride_through_attacks.append(attack)
        return ride_through_attacks

    def get_abilities():

        abilitylist = []
        for ability in unit.abilities:
            if ability in [Ability.sabotage, Ability.poison, Ability.assassinate]:
                target_positions = enemy_units
            elif ability in [Ability.improve_weapons]:
                target_positions = [pos for pos, target in player_units.items() if target.attack and target.is_melee]
            elif ability == Ability.bribe:
                target_positions = [pos for pos, target in enemy_units.items() if not target.has(Effect.bribed)]

            abilityset = [pos for pos in target_positions if distance(start_at, pos) <= unit.range]

            if not (ability == Ability.assassinate and gamestate.actions_remaining > 1):
                abilitylist += make_ability_actions(abilityset, ability)

        return abilitylist

    def get_berserking_attacks():
        moveset_with_leftover, moveset_no_leftover = action_sets.moves_sets(start_at, frozenset(units), zoc_blocks, 4, 4)
        return melee_attack_actions(moveset_with_leftover | {start_at})

    def scout_moves():
        moveset = action_sets.moves_set(start_at, frozenset(units), frozenset([]), unit.movement, unit.movement)
        return make_move_actions(moveset)

    player_units = gamestate.player_units
    enemy_units = gamestate.enemy_units
    units = merge(player_units, enemy_units)

    zoc_blocks = frozenset(position for position, enemy_unit in enemy_units.items() if unit.type in enemy_unit.zoc)

    from functools import partial
    make_action = partial(Action, units, start_at)
    is_zoc_block = partial(action_sets.is_zoc_block, zoc_blocks)
    attack_generator_no_zoc_check = partial(action_sets.attack_generator_no_zoc_check, enemy_units, unit)
    attack_generator = partial(action_sets.attack_generator, enemy_units, unit, is_zoc_block)
    get_ranged_attack_tiles = partial(action_sets.ranged_attacks_set, start_at, frozenset(units))

    def get_tiles():
        moveset_with_leftover, moveset_no_leftover = generate_movesets(unit.movement)
        tiles_unit_can_move_to = moveset_with_leftover | moveset_no_leftover
        tiles_unit_can_melee_attack_from = moveset_with_leftover | {start_at}
        return tiles_unit_can_move_to, tiles_unit_can_melee_attack_from

    def get_basic_attacks_and_moves():

        tiles_unit_can_move_to, tiles_unit_can_melee_attack_from = get_tiles()

        tiles_unit_can_range_attack = get_ranged_attack_tiles(unit.range)

        basic_moves = make_move_actions(tiles_unit_can_move_to)

        if unit.is_ranged:
            basic_attacks = ranged_attack_actions(tiles_unit_can_range_attack)
        else:
            basic_attacks = melee_attack_actions(tiles_unit_can_melee_attack_from)

        return basic_attacks, basic_moves

    attacks, moves = get_basic_attacks_and_moves()

    if unit.has(Trait.rage):
        attacks += get_rage_attacks()

    if unit.has(Trait.berserking):
        attacks += get_berserking_attacks()

    if unit.has(Trait.ride_through):
        attacks += get_ride_through_attacks()

    if unit.has_javelin:
        attacks += get_javelin_attacks()

    abilities = get_abilities()

    if unit.has(Trait.scouting):
        moves = scout_moves()

    if unit.has(Trait.defence_maneuverability):
        moves, attacks = get_defence_maneuverability_actions()

    if unit.has(State.extra_action):
        moves, attacks = get_extra_actions()

    if melee_frozen(gamestate.enemy_units, start_at):
        moves = []

    if not can_attack_with_unit(gamestate, unit) or unit.attack == 0:
        attacks = []

    return moves + attacks + abilities


def can_use_unit(unit, is_extra_action):
    if unit.has(Effect.poisoned) or unit.has(State.recently_bribed):
        return False
    elif is_extra_action:
        return unit.has(State.extra_action)
    else:
        return not unit.has(State.used)


def melee_frozen(enemy_units, start_at):
    return any(pos for pos in start_at.adjacent_tiles() if unit_with_attribute_at(pos, Trait.melee_freeze, enemy_units))


def can_attack_with_unit(gamestate, unit):
    return not (gamestate.actions_remaining == 1 and unit.has(Trait.double_attack_cost)) \
        and not unit.has(Effect.attack_frozen)
