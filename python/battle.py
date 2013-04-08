def attack_successful(action):
    
    attack = get_attack_rating(action.unit, action.target_unit, action)
    
    return action.rolls[0] <= attack


def defence_successful(action):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating)
    
    return action.rolls[1] <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating):
    
    defence_rating = defending_unit.defence
    
    defence_rating += defending_unit.defence_counters
    
    if attacking_unit.type in defending_unit.dbonus:
        defence_rating += defending_unit.dbonus[attacking_unit.type]

    if hasattr(defending_unit, "improved_weapons"):
        defence_rating += 1

    if hasattr(defending_unit, "shield") and attacking_unit.range == 1:
        defence_rating += 1

    if attack_rating > 6:
        defence_rating = defending_unit.defence - attack_rating + 6
    
    if hasattr(defending_unit, "sabotaged"):
        defence_rating = 0
    
    return defence_rating


def get_attack_rating(attacking_unit, defending_unit, action):
    
    attack = attacking_unit.attack
    
    attack += attacking_unit.attack_counters
    
    if hasattr(attacking_unit, "is_crusading"):
        attack += 1
    
    if hasattr(action, "lancing"):
        attack += 2
    
    if hasattr(attacking_unit, "bribed"):
        attack += 1

    if hasattr(action, "high_morale"):
        attack += 2

    if hasattr(attacking_unit, "improved_weapons"):
        attack += 3
 
    if defending_unit.type in attacking_unit.abonus:
        attack += attacking_unit.abonus[defending_unit.type]
    
    return attack


def get_outcome(action):
    attacking_unit = action.unit_reference
    defending_unit = action.target_reference

    attack = get_attack_rating(attacking_unit, defending_unit, action)
    defence = get_defence_rating(attacking_unit, defending_unit, attack)

    if action.rolls[0] <= attack:
        if action.rolls[1] <= defence:
            return "Defend"
        else:
            return" Win"
    else:
        return " Miss"
