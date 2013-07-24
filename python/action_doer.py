from __future__ import division
import random as rnd
import battle


board = [(column, row) for column in range(1, 6) for row in range(1, 9)]


def out_of_board_vertical(position):
    return position[1] < board[1][0] or position[1] > board[1][-1]


def out_of_board_horizontal(position):
    return position[0] < board[0][0] or position[0] > board[0][-1]


def do_action(gamestate, action, controller=None, unit=None):

    def prepare_extra_actions(action, unit):

        if hasattr(unit, "charioting"):
            unit.movement_remaining = unit.movement - distance(action.start_position, action.end_position)
            if action.is_attack():
                unit.movement_remaining -= 1
            unit.extra_action = True

        if hasattr(unit, "samuraiing"):
            unit.movement_remaining = unit.movement - distance(action.start_position, action.final_position)
            unit.extra_action = True

    def update_actions_remaining(action):

        if getattr(gamestate, "extra_action"):
            return

        gamestate.decrement_actions_remaining()

        if hasattr(action, "double_cost"):
            gamestate.decrement_actions_remaining()

    def secondary_action_effects(action, unit):
        if hasattr(unit, "attack_cooldown") and action.is_attack():
            unit.attack_frozen = unit.attack_cooldown

        if hasattr(action.unit, "double_attack_cost") and action.is_attack():
            action.double_cost = True

    if not unit:
        action.unit = gamestate.player_units()[action.start_position]
        unit = action.unit
    else:
        action.unit = unit

    add_target(action, gamestate.opponent_units(), gamestate.player_units())

    secondary_action_effects(action, unit)

    update_actions_remaining(action)

    unit.used = True

    gain_xp(unit)

    if action.start_position in gamestate.player_units():
        gamestate.player_units()[action.end_position] = gamestate.player_units().pop(action.start_position)

    if action.is_attack():
        if hasattr(action, "push"):
            settle_attack_push(action, gamestate.opponent_units(), gamestate.player_units())
        else:
            settle_attack(action, gamestate.opponent_units(), controller)

    if action.is_ability():
        settle_ability(action, gamestate.opponent_units(), gamestate.player_units())

    if getattr(gamestate, "extra_action"):
        del unit.extra_action
        del unit.movement_remaining
    else:
        prepare_extra_actions(action, unit)

    for sub_action in action.sub_actions:
        do_action(gamestate, sub_action, controller, unit)

    if action.end_position in gamestate.player_units():
        gamestate.player_units()[action.final_position] = gamestate.player_units().pop(action.end_position)

    if hasattr(gamestate, "extra_action"):
        gamestate.extra_action = False

    if hasattr(unit, "extra_action"):
        gamestate.current_player().extra_action = True


def settle_attack_push(action, enemy_units, player_units):

    if not action.rolls:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        action.rolls = rolls

    if battle.attack_successful(action):

        push_position = action.push_direction.move(action.attack_position)

        if not battle.defence_successful(action):
            action.outcome = "Success"

            gain_xp(action.unit)

            if hasattr(action.target_unit, "extra_life"):
                del action.target_unit.extra_life

                if not out_of_board_vertical(push_position):
                    update_final_position(action)
                    if push_position in player_units or push_position in enemy_units or out_of_board_horizontal(push_position):
                        del enemy_units[action.attack_position]
                    else:
                        enemy_units[push_position] = enemy_units.pop(action.attack_position)

            else:
                update_final_position(action)
                del enemy_units[action.attack_position]

        else:
            if not out_of_board_vertical(push_position):
                action.outcome = "Push"
                update_final_position(action)
                if push_position in player_units or push_position in enemy_units or out_of_board_horizontal(push_position):
                    del enemy_units[action.attack_position]

                else:
                    enemy_units[push_position] = enemy_units.pop(action.attack_position)

            else:
                action.outcome = "Failure"
    else:
        action.outcome = "Failure"


def settle_attack(action, enemy_units, controller):

    if not action.rolls:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        action.rolls = rolls

    if battle.attack_successful(action) and not battle.defence_successful(action):

        action.outcome = "Success"

        if hasattr(action.target_unit, "extra_life"):
            del action.target_unit.extra_life
        else:
            del enemy_units[action.attack_position]
            if action.unit.range == 1 and controller:
                controller.view.draw_game(controller.gamestate)
                controller.draw_action = False

            update_final_position(action, controller)

    else:
        action.outcome = "Failure"


def settle_ability(action, enemy_units, player_units):

    def sabotage():
        action.target_unit.sabotaged = True

    def poison():
        if not hasattr(action.target_unit, "frozen"):
            action.target_unit.frozen = 3
        else:
            action.target_unit.frozen = max(action.target_unit.frozen, 3)

    def improve_weapons():
        action.target_unit.improved_weapons = True

    def bribe():
        position = action.ability_position
        player_units[position] = enemy_units.pop(position)
        player_units[position].bribed = True

    locals()[action.ability]()


def add_target(action, enemy_units, player_units):
    if action.is_attack():
        action.target_unit = enemy_units[action.attack_position]
    elif action.is_ability():
        if action.ability_position in enemy_units:
            action.target_unit = enemy_units[action.ability_position]
        elif action.ability_position in player_units:
            action.target_unit = player_units[action.ability_position]

    for sub_action in action.sub_actions:
        add_target(sub_action, enemy_units, player_units)


def update_final_position(action, controller=None):

    if action.unit.range == 1 and controller:
        move_with_attack = controller.ask_about_move_with_attack(action)
    else:
        move_with_attack = action.move_with_attack

    if move_with_attack:
        action.final_position = action.attack_position


def gain_xp(unit):
    if not unit.xp_gained_this_round and unit.upgrades:
        unit.xp += 1
        unit.xp_gained_this_round = True


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
