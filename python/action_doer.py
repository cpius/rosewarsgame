from __future__ import division
import random as rnd
import action_getter
import battle


board = [(i, j) for i in range(1, 6) for j in range(1, 9)]


def out_of_board_vertical(pos):
    return pos[1] < board[1][0] or pos[1] > board[1][-1]


def out_of_board_horizontal(pos):
    return pos[0] < board[0][0] or pos[0] > board[0][-1]


def do_action(action, enemy_units, player_units, opponent, player, unit=None):

    def player_has_won(action, unit, enemy_units, opponent):
        return (action.finalpos[1] == opponent.backline and not hasattr(unit, "bribed")) or \
               (not enemy_units and not action.ability == "bribe")

    def prepare_extra_actions(action, unit):

        def charioting():
            if not hasattr(unit, "extra_action"):
                unit.movement_remaining = unit.movement - distance(action.startpos, action.endpos)
                if action.is_attack and not (action.move_with_attack and action.outcome == "Success"):
                    unit.movement_remaining -= 1
                unit.extra_action = True
            else:
                del unit.extra_action

        def samuraiing():
            if not hasattr(unit, "extra_action"):
                unit.movement_remaining = unit.movement - distance(action.startpos, action.endpos)
                unit.extra_action = True
            else:
                del unit.extra_action

        for attribute in ["charioting", "samuraiing"]:
            if hasattr(unit, attribute):
                locals()[attribute]()

    def update_actions_remaining(action, player):

        if not hasattr(player, "extra_action") and not hasattr(player, "sub_action"):
            player.actions_remaining -= 1
            if hasattr(action, "double_cost"):
                player.actions_remaining -= 1

    def secondary_action_effects(action, unit):
        if hasattr(unit, "attack_cooldown") and action.is_attack:
            unit.attack_frozen = unit.attack_cooldown

        if hasattr(action.unit, "double_attack_cost") and action.is_attack:
            action.double_cost = True

    if not unit:
        action.unit = player_units[action.startpos]
        unit = action.unit
    else:
        action.unit = unit

    add_target(action, enemy_units, player_units)

    secondary_action_effects(action, unit)

    update_actions_remaining(action, player)

    unit.used = True

    if action.is_attack:
        if hasattr(action, "push"):
            settle_attack_push(action, enemy_units, player_units)
        else:
            settle_attack(action, enemy_units)

    if action.is_ability:
        settle_ability(action, enemy_units, player_units)

    prepare_extra_actions(action, unit)

    for sub_action in action.sub_actions:
        player.sub_action = True
        do_action(sub_action, enemy_units, player_units, opponent, player, unit)
        del player.sub_action

    if action.startpos in player_units:
        player_units[action.finalpos] = player_units.pop(action.startpos)

    if player_has_won(action, unit, enemy_units, opponent):
        player.won = True

    if hasattr(player, "extra_action"):
        del player.extra_action
    else:
        all_extra_actions = action_getter.get_extra_actions(enemy_units, player_units, player)
        if len(all_extra_actions) > 1:
            player.extra_action = True

    return enemy_units, player_units, player


def settle_attack_push(action, enemy_units, player_units):

    if not action.rolls:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        action.rolls = rolls

    if battle.attack_successful(action):

        pushpos = action.push_direction.move(action.attackpos)

        if not battle.defence_successful(action):
            action.outcome = "Success"

            gain_xp(action.unit)

            if hasattr(action.target_unit, "extra_life"):
                del action.target_unit.extra_life

                if not out_of_board_vertical(pushpos):
                    update_finalpos(action)
                    if pushpos in player_units or pushpos in enemy_units or out_of_board_horizontal(pushpos):
                        del enemy_units[action.attackpos]
                    else:
                        enemy_units[pushpos] = enemy_units.pop(action.attackpos)

            else:
                update_finalpos(action)
                del enemy_units[action.attackpos]

        else:
            if not out_of_board_vertical(pushpos):
                action.outcome = "Push"
                update_finalpos(action)
                if pushpos in player_units or pushpos in enemy_units or out_of_board_horizontal(pushpos):
                    gain_xp(action.unit)
                    del enemy_units[action.attackpos]

                else:
                    enemy_units[pushpos] = enemy_units.pop(action.attackpos)

            else:
                action.outcome = "Failure"
    else:
        action.outcome = "Failure"


def settle_attack(action, enemy_units):

    if not action.rolls:
        rolls = [rnd.randint(1, 6), rnd.randint(1, 6)]
        action.rolls = rolls

    if battle.attack_successful(action) and not battle.defence_successful(action):

        action.outcome = "Success"

        gain_xp(action.unit)

        if hasattr(action.target_unit, "extra_life"):
            del action.target_unit.extra_life
        else:
            del enemy_units[action.attackpos]
            update_finalpos(action)

    else:
        action.outcome = "Failure"


def settle_ability(action, enemy_units, player_units):

    def sabotage():
        action.target_unit.sabotaged = True

    def poison():
        if not hasattr(action.target_unit, "frozen"):
            action.target_unit.frozen = 2
        else:
            action.target_unit.frozen = max(action.target_unit.frozen, 2)

    def improve_weapons():
        action.target_unit.improved_weapons = True

    def bribe():
        pos = action.attackpos
        player_units[pos] = enemy_units.pop(pos)
        player_units[pos].bribed = True

    locals()[action.ability]()


def add_target(action, enemy_units, player_units):
    if action.is_attack:
        action.target_unit = enemy_units[action.attackpos]
    elif action.is_ability:
        if action.attackpos in enemy_units:
            action.target_unit = enemy_units[action.attackpos]
        elif action.attackpos in player_units:
            action.target_unit = player_units[action.attackpos]

    for sub_action in action.sub_actions:
        add_target(sub_action, enemy_units, player_units)



def update_finalpos(action):
    if action.move_with_attack:
        action.finalpos = action.attackpos


def gain_xp(unit):
    if not unit.xp_gained_this_round:
        unit.xp += 1
        unit.xp_gained_this_round = True


def distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
