from common import *


def attack_successful(action, rolls, gamestate):
    
    attack = get_attack_rating(action.unit, action.target_unit, action, gamestate.player_units)
    
    return rolls.attack <= attack


def defence_successful(action, rolls, gamestate):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action, gamestate.player_units)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating, action, gamestate.enemy_units)
    
    return rolls.defence <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating, action, enemy_units):

    def defence_adjusters(defence):

        defence += 2 * int(attacking_unit.is_melee() and defending_unit.has(Trait.big_shield))
        defence += int(action.is_crusading(enemy_units, 2))
        if attacking_unit.type in defending_unit.defence_bonuses:
            defence += defending_unit.defence_bonuses[attacking_unit.type]
        defence += int(defending_unit.has(Effect.improved_weapons))
        defence += int(attacking_unit.is_melee() and defending_unit.has(Trait.melee_expert))
        defence -= int(attacking_unit.has(Trait.pikeman_specialist) and defending_unit.name == "Pikeman")
        defence += int(attacking_unit.is_ranged() and defending_unit.has(Trait.tall_shield))
        defence += int(defending_unit.has(Trait.cavalry_specialist) and attacking_unit.type == Type.Cavalry)
        defence += int(defending_unit.has(Trait.siege_weapon_specialist) and attacking_unit.type == Type.Siege_Weapon)

        return defence

    def defence_setters(defence):
        if attacking_unit.has(Trait.sharpshooting):
            return 1

        if defending_unit.has(Effect.sabotaged, 1):
            return 0

        if defending_unit.has(Effect.sabotaged, 2):
            return -1

        return defence

    defence = defending_unit.defence

    defence = defence_adjusters(defence)

    defence = defence_setters(defence)

    if attack_rating > 6:
        defence = defence - attack_rating + 6

    return defence


def get_attack_rating(attacking_unit, defending_unit, action, player_units):

    def attack_adjusters():
        attack = 0
        attack += action.lancing()
        attack += int(action.is_crusading(player_units))
        attack += int(action.is_crusading(player_units, 2))
        attack += 2 * int(action.has_high_morale(player_units))
        attack += int(attacking_unit.has(Effect.bribed))
        attack += 3 * int(attacking_unit.has(Effect.improved_weapons, level=1))
        attack += 2 * int(attacking_unit.has(Effect.improved_weapons, level=2))
        if defending_unit.type in attacking_unit.attack_bonuses:
            attack += attacking_unit.attack_bonuses[defending_unit.type]
        attack -= int(defending_unit.has(Trait.pikeman_specialist) and attacking_unit.name == "Pikeman")
        attack += int(defending_unit.is_melee() and attacking_unit.has(Trait.melee_expert))
        attack -= int(attacking_unit.has(Trait.far_sighted) and distance(action.end_at, action.target_at) < 4)
        attack += int(attacking_unit.has(Trait.cavalry_specialist) and defending_unit.type == Type.Cavalry)
        attack += int(attacking_unit.has(Trait.siege_weapon_specialist) and defending_unit.type == Type.Siege_Weapon)
        attack += 3 * int(attacking_unit.has(Trait.fire_arrows) and defending_unit.type == Type.Siege_Weapon)
        attack += 2 * int(attacking_unit.has(Trait.flanking) and defending_unit.type == Type.Infantry)

        return attack

    attack = attacking_unit.attack
    attack += attack_adjusters()

    return attack
