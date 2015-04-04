from gamestate.action import Action
from gamestate.gamestate_library import *
from itertools import product
import gamestate.action_sets as action_sets


class UnitActions:
    def __init__(self, unit, position, gamestate, bonus_tiles):
        self.unit = unit
        self.start_at = position
        self.gamestate = gamestate
        self.actions = set()
        self.player_units = gamestate.player_units
        self.enemy_units = gamestate.enemy_units
        self.units = gamestate.all_units()
        self.unit_positions = frozenset(self.units)
        self.bonus_tiles = bonus_tiles
        self.zoc_blocks = None
        self.moveset_with_leftover = None
        self.moveset_without_leftover = None
        self.moveset = None

    def get_all_actions(self):
        unit = self.unit

        self.set_zoc_blocks()
        self.set_movesets()

        if self.gamestate.is_extra_action():
            return self.get_extra_actions()

        abilities = self.get_abilities()

        if unit.is_ranged and not unit.abilities:
            attacks = self.get_ranged_attacks()
        elif unit.is_melee:
            attacks = self.get_melee_attacks()
        else:
            attacks = set()

        moves = self.get_moves()

        if unit.has_javelin:
            attacks |= self.get_javelin_attacks()

        if unit.has(Trait.berserking):
            attacks |= self.get_berserking_attacks()

        if unit.has(Trait.scouting):
            moves |= self.get_scouting_moves()

        if unit.has(Trait.rage):
            attacks |= self.get_rage_attacks()

        if unit.has(Trait.ride_through):
            attacks |= self.get_ride_through_attacks()

        if unit.has(Trait.defence_maneuverability):
            attacks, moves = self.get_defence_maneuverability_actions()

        return moves | attacks | abilities

    def set_movesets(self, movement=None, zoc_blocks=None):
        """
        :param movement: The number of tiles the unit can move
        :param zoc_blocks: Positions on the board with units exerting ZOC against the unit.
        Sets three moveset attributes:
        moveset_with_leftover: The tiles the unit can move to, and still have leftover movement to make an attack.
        moveset_without_leftover: The tiles it can move to, with no leftover movement to make an attack.
        moveset: All tiles the unit can move to.
        """
        movement = movement if movement else self.unit.movement
        zoc_blocks = zoc_blocks if zoc_blocks is not None else self.zoc_blocks

        moves_sets = action_sets.moves_sets(self.start_at, self.unit_positions, zoc_blocks, movement, movement)
        self.moveset_with_leftover, self.moveset_without_leftover = moves_sets
        self.moveset = self.moveset_with_leftover | self.moveset_without_leftover

    def set_zoc_blocks(self):
        """
        Saves the positions containing enemy units that exert ZOC against the unit to self.zoc_blocks
        """
        zoc_blocks = set()
        for position, enemy_unit in self.enemy_units.items():
            if enemy_unit.has(Trait.zoc_all):
                zoc_blocks.add(position)
            elif enemy_unit.has(Trait.zoc_cavalry) and self.unit.type == Type.Cavalry:
                zoc_blocks.add(position)
        self.zoc_blocks = frozenset(zoc_blocks)

    def get_abilities(self):
        abilities = set()
        for ability in self.unit.abilities:
            if ability == Ability.assassinate and self.gamestate.actions_remaining == 2:
                continue

            if ability in [Ability.sabotage, Ability.poison, Ability.assassinate]:
                possible_targets = self.enemy_units
            elif ability in [Ability.improve_weapons]:
                possible_targets = [pos for pos, target in self.player_units.items() if target.is_melee]
            elif ability == Ability.bribe:
                possible_targets = [pos for pos, target in self.enemy_units.items() if not target.has(Effect.bribed)]

            targets_in_range = [pos for pos in possible_targets if distance(self.start_at, pos) <= self.unit.range]
            abilities |= {self.make_action(target_at=target, ability=ability) for target in targets_in_range}

        return abilities

    def get_moves(self):
        return {self.make_action(end_at=position) for position in self.moveset}

    def can_take_tile(self, position, attack_position, direction, zoc_blocks):
        """
        :param position: The position of the unit.
        :param attack_position: The position the unit is attacking
        :param direction: The direction from position to attack_position
        :param zoc_blocks: Tiles with opponents units exerting zoc
        :return: Whether the unit is allowed to make a move_with_attack
        """
        zoc_blocked = zoc_block(position, direction, zoc_blocks)
        extra_life_blocked = self.enemy_units[attack_position].has_extra_life
        if extra_life_blocked and self.unit.has(Trait.push):
            extra_life_blocked = False
            position_behind_enemy_unit = attack_position.move(direction)
            if position_behind_enemy_unit in self.enemy_units:
                extra_life_blocked = True
        return not (zoc_blocked or extra_life_blocked)

    def get_melee_attacks(self, zoc_blocks=None, moveset=None, allow_move_with_attack=True):
        """
        :param zoc_blocks: Tiles with opponents units exerting zoc
        :param moveset: The tiles a unit can move to and attack from
        :param allow_move_with_attack: Whether a move with attack is allowed if not blocked
        :return All attack actions the unit can perform with move_with_attack as True/False
        """
        zoc_blocks = zoc_blocks if zoc_blocks else self.zoc_blocks
        moveset = moveset if moveset else self.moveset_with_leftover
        moveset = moveset | {self.start_at}
        attacks = set()
        for position, direction in product(moveset, directions):
            new_position = position.move(direction)
            if new_position in self.enemy_units:
                if allow_move_with_attack and self.can_take_tile(position, new_position, direction, zoc_blocks):
                    attacks.add(self.make_action(end_at=position, target_at=new_position, move_with_attack=True))
                attacks.add(self.make_action(end_at=position, target_at=new_position, move_with_attack=False))
        return attacks

    def get_targets_in_range(self, range=None, units=None):
        if not range:
            range = self.unit.range
        if not units:
            units = self.enemy_units
        return {pos for pos in board_tiles if pos in units and distance(pos, self.start_at) <= range}

    def get_ranged_attacks(self):
        target_tiles = self.get_targets_in_range()
        return {self.make_action(end_at=self.start_at, target_at=target) for target in target_tiles}

    def make_action(self, end_at=None, target_at=None, move_with_attack=None, ability=None):
        if not end_at:
            end_at = self.start_at
        return Action(self.units, self.start_at, end_at, target_at, move_with_attack, ability)

    def get_javelin_attacks(self):
        return {self.make_action(target_at=target, move_with_attack=False) for target in self.get_targets_in_range(3)}

    def get_berserking_attacks(self):
        self.set_movesets(movement=4)
        return self.get_melee_attacks()

    def get_scouting_moves(self):
        self.set_movesets(zoc_blocks=frozenset())
        return self.get_moves()

    def get_rage_attacks(self):
        return self.get_melee_attacks(set(), self.moveset_without_leftover, allow_move_with_attack=False)

    def get_ride_through_attacks(self):
        attacks = set()
        for direction in directions:
            one_tile_away = self.start_at.move(direction)
            if not one_tile_away:
                continue
            two_tiles_away = one_tile_away.move(direction)
            if not two_tiles_away:
                continue
            if one_tile_away in self.enemy_units and two_tiles_away not in self.units:
                attacks.add(self.make_action(end_at=two_tiles_away, target_at=one_tile_away, move_with_attack=False))
        return attacks

    def get_defence_maneuverability_actions(self):
        self.set_movesets(movement=2)
        moves = {move for move in self.get_moves() if abs(move.start_at.row - move.end_at.row) < 2}
        attacks = {attack for attack in self.get_melee_attacks() if abs(attack.start_at.row - attack.target_at.row) < 2}

        return moves, attacks

    def get_combat_agility_attacks(self):
        return self.get_melee_attacks(allow_move_with_attack=self.unit.get(State.movement_remaining))

    def get_extra_actions(self):
        moves, attacks = set(), set()
        if self.unit.has(Trait.swiftness):
            self.set_movesets(movement=self.unit.get(State.movement_remaining))
            moves = self.get_moves()

        if self.unit.has(Trait.combat_agility):
            attacks = self.get_combat_agility_attacks()

        return moves | attacks


def get_bonus_tiles(gamestate):
    """
    :param gamestate: The gamestate
    :return: The set of tiles that are affected by a friendly Crusader or Flag Bearer.
    """
    bonus_tiles = {
        Trait.crusading: {
            1: set(),
            2: set()
        },
        Trait.flag_bearing: set()
    }

    for pos, unit in gamestate.player_units.items():
        if unit.has(Trait.crusading, 1):
            bonus_tiles[Trait.crusading][1] |= pos.surrounding_tiles()
        if unit.has(Trait.crusading, 2):
            bonus_tiles[Trait.crusading][2] |= pos.surrounding_tiles()
        if unit.has(Trait.flag_bearing, 1):
            bonus_tiles[Trait.flag_bearing] |= pos.adjacent_tiles()
        if unit.has(Trait.flag_bearing, 2):
            bonus_tiles[Trait.flag_bearing] |= pos.surrounding_tiles()

    return bonus_tiles


def get_actions(gamestate):

    if not gamestate.actions_remaining and not gamestate.is_extra_action():
        return []

    bonus_tiles = get_bonus_tiles(gamestate)
    actions = set()
    for position, unit in gamestate.player_units.items():
        if can_use_unit(unit, gamestate):
            unit_actions = UnitActions(unit, position, gamestate, bonus_tiles)
            actions |= unit_actions.get_all_actions()

    return actions


def can_use_unit(unit, gamestate):
    if unit.has(Effect.poisoned) or unit.has(State.recently_bribed):
        return False
    elif unit.has(Trait.double_attack_cost) and gamestate.actions_remaining < 2:
        return False
    elif gamestate.is_extra_action():
        return unit.has(State.extra_action)
    else:
        return not unit.has(State.used)
