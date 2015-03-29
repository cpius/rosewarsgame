from gamestate.gamestate_library import *
from game.game_library import merge


class Board():
    def __init__(self, units):
        self.units = units

    def all_units(self):
        return merge(*self.units)

    @property
    def player_units(self):
        return self.units[0]

    @property
    def enemy_units(self):
        return self.units[1]

    def flip_all_units(self):
        self.units = [flip_units(self.player_units), flip_units(self.enemy_units)]

    def is_ended(self):
        def unit_on_opponents_backline():
            return any(unit for position, unit in self.player_units.items() if position.row == 8
                       and not unit.has(Effect.bribed))

        def no_enemy_units():
            return not self.enemy_units and not any(unit for unit in self.player_units.values() if
                                                    unit.has(Effect.bribed))

        return unit_on_opponents_backline() or no_enemy_units()

    def is_extra_action(self):
        return any(unit for unit in self.player_units.values() if unit.has(State.extra_action))

    def get_upgradeable_unit(self):
        for position, unit in self.player_units.items():
            if unit.should_be_upgraded():
                return position, unit

    def delete_unit_at(self, position):
        if position in self.player_units:
            del self.player_units[position]
        else:
            del self.enemy_units[position]

    def move_unit(self, start_position, end_position):
        if start_position in self.player_units:
            self.player_units[end_position] = self.player_units.pop(start_position)
        else:
            self.enemy_units[end_position] = self.enemy_units.pop(start_position)

    def change_unit_owner(self, position):
        self.player_units[position] = self.enemy_units.pop(position)

    def pass_extra_action(self):
        for unit in self.player_units.values():
            unit.remove(State.extra_action)
            unit.remove(State.movement_remaining)
