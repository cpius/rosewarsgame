from gamestate.gamestate_library import *


def get_defence_adjusters(attacking_unit, defending_unit, action, gamestate):

    defence_adjusters = 0

    if defending_unit.has(Effect.improved_weapons):
        defence_adjusters += 1

    if attacking_unit.type == Type.War_Machine and defending_unit.has(Trait.sturdy_helmet):
        defence_adjusters += 1

    if defending_unit.has(Trait.cavalry_specialist) and attacking_unit.type == Type.Cavalry:
        defence_adjusters += 1

    if action.is_javelin_throw:
        defence_adjusters -= 1

    return defence_adjusters


def get_defence_setters(attacking_unit, defending_unit):

    defence_setters = []

    if defending_unit.has(Effect.sabotaged, 1) or defending_unit.has(Effect.sabotaged, 2):
        defence_setters.append(0)

    return defence_setters


def get_defence(action, attack, gamestate):

    attacking_unit = action.unit
    defending_unit = action.target_unit

    defence_setters = get_defence_setters(attacking_unit, defending_unit)

    if defence_setters:
        defence = min(defence_setters)
    else:
        defence = defending_unit.defence + get_defence_adjusters(attacking_unit, defending_unit, action, gamestate)

    if attack > 6:
        defence = defence - attack + 6

    return defence


def get_attack(action, gamestate, is_sub_action=False):

    attacking_unit = action.unit
    defending_unit = action.target_unit

    attack = attacking_unit.attack

    if lancing(action):
        attack += 3

    if flanking(action):
        attack += 2 * attacking_unit.get(Trait.flanking)

    if not attacking_unit.type == Type.War_Machine and action.start_at in gamestate.bonus_tiles[Trait.crusading][1]:
        attack += 1

    if not attacking_unit.type == Type.War_Machine and action.start_at in gamestate.bonus_tiles[Trait.crusading][2]:
        attack += 2

    if (action.end_at in gamestate.bonus_tiles[Trait.flag_bearing] and not attacking_unit.unit == Unit.Flag_Bearer
            and not (action.is_javelin_throw or attacking_unit.is_ranged)):
        attack += 2

    if hasattr(action, "high_morale"):
        attack += 2

    if attacking_unit.has(Effect.bribed, 1):
        attack += 1

    if attacking_unit.has(Effect.bribed, 2):
        attack += 2

    if attacking_unit.has(Effect.improved_weapons, 1):
        attack += 3

    if attacking_unit.has(Effect.improved_weapons, 2):
        attack += 2

    if attacking_unit.has(Trait.arrows) and defending_unit.type == Type.Infantry:
        attack += 1

    if attacking_unit.has(Trait.cavalry_specialist) and defending_unit.type == Type.Cavalry:
        attack += 1

    if attacking_unit.has(Trait.fire_arrows) and defending_unit.type == Type.War_Machine:
        attack += 3

    return attack


def lancing(action):
    if action.unit.has(Trait.lancing, 1) and action.is_attack and distance_to_target(action) >= 3:
        return 3
    elif action.unit.has(Trait.lancing, 2) and action.is_attack and distance_to_target(action) >= 2:
        return 3
    else:
        return 0


def distance_to_target(action):
    return distance(action.start_at, action.target_at)


def flanking(action):
    if not action.unit.has(Trait.flanking) or action.target_unit.has(State.flanked):
        return False
    attack_direction = action.end_at.get_direction_to(action.target_at)
    if attack_direction == Direction.up:
        return False

    return True


def is_win(action, rolls, gamestate, is_sub_action=False):
    return attack_successful(action, rolls, gamestate, is_sub_action) and not \
        defence_successful(action, rolls, gamestate, is_sub_action)


def attack_successful(action, rolls, gamestate, is_sub_action=False):
    attack = get_attack(action, gamestate, is_sub_action)
    return rolls.attack <= attack


def defence_successful(action, rolls, gamestate, is_sub_action=False):
    attack = get_attack(action, gamestate, is_sub_action)
    defence = get_defence(action, attack, gamestate)
    return rolls.defence <= defence


def get_outcome_string(action, outcome, gamestate, is_sub_action):
    if is_win(action, outcome, gamestate, is_sub_action):
        return "WIN"
    elif attack_successful(action, outcome, gamestate, is_sub_action) and action.is_push:
        return "PUSH"
    elif not attack_successful(action, outcome, gamestate, is_sub_action):
        return "MISS"
    else:
        return "DEFEND"


def assassin_kills_target(rolls, level):
    if level == 1:
        return rolls.defence > 2
    else:
        return True


def assassin_dies(rolls):
    return rolls.defence > 3

