def attack_successful(u1, u2, action, rolls):
    
    attack = get_attack(u1, u2, action)
    if attack < 1:
        attack = 1
    
    return rolls[0] >= attack


def defence_successful(u1,u2,action, rolls):

    attack = get_attack(u1, u2, action)
    if attack < 1:
        attack = 1
    defence = get_defence(u1, u2, attack, action)
    
    return rolls[1] <= defence
    

def get_defence(a, d, attack, action):
    
    defence = d.defence
    
    defence += d.dcounters
    
    if a.type in d.dbonus:
        defence += d.dbonus[a.type]
    
    if attack < 1:
        defence = d.defence + attack -1
    
    return defence


def get_attack(a, d, action):
    
    attack = a.attack
    
    attack -= a.acounters
    
    if a.is_crusading:
        attack += 1
    
    if hasattr(action, "abonus"):
        attack -= action.abonus  
    
    if d.type in a.abonus:
        attack -= a.abonus[d.type]
    
    return attack