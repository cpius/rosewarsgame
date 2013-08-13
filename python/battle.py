from common import *


def attack_successful(action, rolls, gamestate):
    
    attack = get_attack_rating(action.unit, action.target_unit, action, gamestate.player_units)
    
    return rolls.attack <= attack


def defence_successful(action, rolls, gamestate):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action, gamestate.player_units)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating, action, gamestate.enemy_units)
    
    return rolls.defence <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating, action, enemy_units):

    def big_shield():
        return 2 * int(attacking_unit.is_melee() and defending_unit.has(Trait.big_shield))

    def crusading_II_defence():
        return int(action.is_crusading_II_defence(enemy_units))

    def defence_bonuses():
        return defending_unit.defence_bonuses[attacking_unit.type] if \
            attacking_unit.type in defending_unit.defence_bonuses else 0

    def improved_weapons():
        improvements = {State.improved_weapons: 1, State.improved_weapons_II_A: 1}
        return sum(value for trait, value in improvements.items() if defending_unit.has(trait))

    def melee_expert():
        return int(attacking_unit.is_melee() and defending_unit.has(Trait.melee_expert))

    def pikeman_specialist():
        return - int(attacking_unit.has(Trait.pikeman_specialist) and defending_unit.name == "Pikeman")

    def tall_shield():
        return int(attacking_unit.is_ranged() and defending_unit.has(Trait.tall_shield))

    def sharpshooting(defence):
        return 1 if attacking_unit.has(Trait.sharpshooting) else defence

    def sabotaged(defence):
        return 0 if any(defending_unit.has(effect) for effect in [State.sabotaged, State.sabotaged_II]) else defence

    def cavalry_specialist():
        return int(defending_unit.has(Trait.cavalry_specialist) and attacking_unit.type == Type.Cavalry)

    def siege_weapon_specialist():
        return int(defending_unit.has(Trait.siege_weapon_specialist) and attacking_unit.type == Type.Siege_Weapon)

    def adjust_for_high_attack(defence):
        return defence - attack_rating + 6 if attack_rating > 6 else defence

    defence_adjusters = ["big_shield", "crusading_II_defence", "defence_bonuses", "improved_weapons", "melee_expert",
                         "pikeman_specialist", "tall_shield", "cavalry_specialist", "siege_weapon_specialist"]

    defence_setters = ["sharpshooting", "sabotaged"]

    defence = defending_unit.defence

    defence += sum([locals()[factor]() for factor in defence_adjusters])

    defence = min([locals()[factor](defence) for factor in defence_setters])

    defence = adjust_for_high_attack(defence)

    return defence


def get_attack_rating(attacking_unit, defending_unit, action, player_units):

    def lancing():
        effects = {"is_lancing": 2, "is_lancing_II": 3}
        return sum(value for effect, value in effects.items() if getattr(action, effect)())

    def crusading():
        effects = ["is_crusading", "is_crusading_II_attack"]
        return sum(1 for effect in effects if getattr(action, effect)(player_units))

    def high_morale():
        effects = {"has_high_morale": 2, "has_high_morale_II_A": 2, "has_high_morale_II_B": 3}
        return sum(value for effect, value in effects.items() if getattr(action, effect)(player_units))

    def bribed():
        states = {State.bribed: 1, State.bribed_II: 2}
        return sum(value for state, value in states.items() if attacking_unit.has(state))

    def improved_weapons():
        traits = {State.improved_weapons: 3, State.improved_weapons_II_A: 2}
        return sum(value for trait, value in traits.items() if attacking_unit.has(trait))

    def attack_bonuses():
        return attacking_unit.attack_bonuses[defending_unit.type] if \
            defending_unit.type in attacking_unit.attack_bonuses else 0

    def pikeman_specialist():
        return - int(defending_unit.has(Trait.pikeman_specialist) and attacking_unit.name == "Pikeman")

    def melee_expert():
        return int(defending_unit.is_melee() and attacking_unit.has(Trait.melee_expert))

    def far_sighted():
        return - int(attacking_unit.has(Trait.far_sighted) and distance(action.end_at, action.target_at) < 4)

    def cavalry_specialist():
        return int(attacking_unit.has(Trait.cavalry_specialist) and defending_unit.type == Type.Cavalry)

    def siege_weapon_specialist():
        return int(attacking_unit.has(Trait.siege_weapon_specialist) and defending_unit.type == Type.Siege_Weapon)

    attack = attacking_unit.attack

    attack_adjusters = ["lancing", "crusading", "high_morale", "bribed", "improved_weapons", "attack_bonuses",
                        "pikeman_specialist", "melee_expert", "cavalry_specialist", "siege_weapon_specialist"]

    attack += sum([locals()[factor]() for factor in attack_adjusters])

    return attack
