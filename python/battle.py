def attack_successful(action):
    
    attack = get_attack(action.unit, action.target_unit, action)
    
    return action.rolls[0] <= attack


def defence_successful(action):

    attack = get_attack(action.unit, action.target_unit, action)
    defence = get_defence(action.unit, action.target_unit, attack, action)
    
    return action.rolls[1] <= defence
    

def get_defence(attacking_unit, defending_unit, attack, action):
    
    defence = defending_unit.defence
    
    defence += defending_unit.dcounters
    
    if attacking_unit.type in defending_unit.dbonus:
        defence += defending_unit.dbonus[attacking_unit.type]

    if hasattr(defending_unit, "improved_weapons"):
        defence += 1

    if hasattr(defending_unit, "shield") and attacking_unit.range == 1:
        defence += 1

    if attack > 6:
        defence = defending_unit.defence - attack + 6
    
    if hasattr(defending_unit, "sabotaged"):
        defence = 0
    
    return defence


def get_attack(attacking_unit, defending_unit, action):
    
    attack = attacking_unit.attack
    
    attack += attacking_unit.acounters
    
    if hasattr(attacking_unit, "is_crusading"):
        attack += 1
    
    if hasattr(action, "lancing"):
        attack += 2
    
    if hasattr(action, "high_morale"):
        attack += 2

    if hasattr(attacking_unit, "improved_weapons"):
        attack += 3
 
    if defending_unit.type in attacking_unit.abonus:
        attack += attacking_unit.abonus[defending_unit.type]
    
    return attack
