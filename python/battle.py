from outcome import Outcome, SubOutcome


def attack_successful(action, rolls):
    
    attack = get_attack_rating(action.unit, action.target_unit, action)
    
    return rolls[0] <= attack


def defence_successful(action, rolls):

    attack_rating = get_attack_rating(action.unit, action.target_unit, action)
    defence_rating = get_defence_rating(action.unit, action.target_unit, attack_rating)
    
    return rolls[1] <= defence_rating
    

def get_defence_rating(attacking_unit, defending_unit, attack_rating):
    
    defence_rating = defending_unit.defence

    if attacking_unit.type in defending_unit.dbonus:
        defence_rating += defending_unit.dbonus[attacking_unit.type]

    if hasattr(defending_unit, "improved_weapons"):
        defence_rating += 1

    if hasattr(defending_unit, "shield") and attacking_unit.range == 1:
        defence_rating += 1

    if hasattr(attacking_unit, "sharpshooting"):
        defence_rating = 1

    if attack_rating > 6:
        defence_rating = defending_unit.defence - attack_rating + 6
    
    if "sabotaged" in defending_unit.variables:
        defence_rating = 0
    
    return defence_rating


def get_attack_rating(attacking_unit, defending_unit, action):
    
    attack = attacking_unit.attack

    if hasattr(attacking_unit, "is_crusading"):
        attack += 1
    
    if action.is_lancing():
        attack += 2

    if action.is_lancing_II():
        attack += 3
    
    if attacking_unit.get_bribed():
        attack += 1

    if hasattr(action, "high_morale"):
        attack += 2

    if hasattr(attacking_unit, "improved_weapons"):
        attack += 3
 
    if defending_unit.type in attacking_unit.abonus:
        attack += attacking_unit.abonus[defending_unit.type]
    
    return attack


def get_outcome(action, outcome):
    sub_outcome = outcome.for_position(action.attack_position)
    if sub_outcome == SubOutcome.MISS:
        return " Miss"
    elif sub_outcome == SubOutcome.DEFEND:
        return " Defend"
    elif sub_outcome == SubOutcome.WIN:
        return " Win"
