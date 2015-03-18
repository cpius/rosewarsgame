from common import *


def get_defence_adjusters(attacking_unit, defending_unit, action, gamestate):

    defence_adjusters = 0

    if attacking_unit.is_melee() and defending_unit.has(Trait.big_shield):
        defence_adjusters += 2

    if "No_Crusader" not in gamestate.ai_factors and is_crusading_defense(action, gamestate.enemy_units, level=2):
        defence_adjusters += 1

    if attacking_unit.type in defending_unit.defence_bonuses:
        defence_adjusters += defending_unit.defence_bonuses[attacking_unit.type]

    if defending_unit.has(Effect.improved_weapons):
        defence_adjusters += 1

    if attacking_unit.is_melee() and defending_unit.has(Trait.melee_expert):
        defence_adjusters += 1

    if attacking_unit.has(Trait.pikeman_specialist) and defending_unit == Unit.Pikeman:
        defence_adjusters += 1

    if attacking_unit.is_ranged() and defending_unit.has(Trait.tall_shield):
        defence_adjusters += 1

    if defending_unit.has(Trait.cavalry_specialist) and attacking_unit.type == Type.Cavalry:
        defence_adjusters += 1

    if defending_unit.has(Trait.war_machine_specialist) and attacking_unit.type == Type.War_Machine:
        defence_adjusters += 1

    if action.is_javelin_throw():
        defence_adjusters -= 1

    return defence_adjusters


def get_defence_setters(attacking_unit, defending_unit):

    defence_setters = []
    if attacking_unit.has(Trait.sharpshooting):
        defence_setters.append(1)

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
        attack += lancing(action)

    if flanking(action):
        attack += 2 * attacking_unit.get_level(Trait.flanking)

    if "No_player_Crusader" not in gamestate.ai_factors and is_crusading_attack(action, gamestate.player_units, 1):
        attack += 1

    if "No_player_Crusader" not in gamestate.ai_factors and is_crusading_attack(action, gamestate.player_units, 2):
        attack += 1

    if "No_FlagBearer" not in gamestate.ai_factors and has_high_morale(action, gamestate.player_units):
        attack += 2

    if attacking_unit.has(Effect.bribed, 1):
        attack += 1

    if attacking_unit.has(Effect.bribed, 2):
        attack += 2

    if attacking_unit.has(Effect.improved_weapons, 1):
        attack += 3

    if attacking_unit.has(Effect.improved_weapons, 2):
        attack += 2

    if defending_unit.type in attacking_unit.attack_bonuses:
        attack += attacking_unit.attack_bonuses[defending_unit.type]

    if defending_unit.has(Trait.pikeman_specialist) and attacking_unit == Unit.Pikeman:
        attack += 1

    if defending_unit.is_melee() and attacking_unit.has(Trait.melee_expert):
        attack += 1

    if attacking_unit.has(Trait.far_sighted) and distance(action.end_at, action.target_at) < 4:
        attack -= 1

    if attacking_unit.has(Trait.cavalry_specialist) and defending_unit.type == Type.Cavalry:
        attack += 1

    if attacking_unit.has(Trait.war_machine_specialist) and defending_unit.type == Type.War_Machine:
        attack += 1

    if attacking_unit.has(Trait.fire_arrows) and defending_unit.type == Type.War_Machine:
        attack += 3

    return attack


def lancing(action):
    if action.unit.has(Trait.lancing, 1) and action.is_attack() and distance_to_target(action) >= 3:
        return 2
    elif action.unit.has(Trait.lancing, 2) and action.is_attack() and distance_to_target(action) >= 4:
        return 3
    else:
        return 0


def distance_to_target(action):
    return distance(action.start_at, action.target_at)


def is_crusading_attack(action, units, level=1):
    return action.unit.is_melee() and (is_surrounding_unit_with(action, units, Trait.crusading, action.start_at, level))


def is_crusading_defense(action, units, level=1):
    return action.unit.is_melee() and (is_surrounding_unit_with(action, units, Trait.crusading, action.target_at, level))


def has_high_morale(action, units):
    return action.unit.is_melee() and (is_adjacent_unit_with(action, units, Trait.flag_bearing, action.end_at) or
                                       is_surrounding_unit_with(action, units, Trait.flag_bearing, action.end_at, 2))


def is_surrounding_unit_with(action, units, attribute, position, level=1):
    return any(unit_with_attribute_at(pos, attribute, units, level) for pos in position.surrounding_tiles() if
               pos != action.start_at)


def is_adjacent_unit_with(action, units, attribute, position, level=1):
    return any(unit_with_attribute_at(pos, attribute, units, level) for pos in position.adjacent_tiles() if
               pos != action.start_at)


def flanking(action):
    if not action.unit.has(Trait.flanking) or action.target_unit.has(State.flanked):
        return False
    attack_direction = action.end_at.get_direction_to(action.target_at)
    if attack_direction == Direction("Up"):
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
    elif attack_successful(action, outcome, gamestate, is_sub_action) and action.is_push():
        return "PUSH"
    elif not attack_successful(action, outcome, gamestate, is_sub_action):
        return "MISS"
    else:
        return "DEFEND"
