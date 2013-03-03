def attack_successful(u1, u2, action, rolls):
    
    attack = get_attack(u1, u2, action)
    
    return rolls[0] >= attack


def defence_successful(u1,u2,action, rolls):

    attack = get_attack(u1, u2, action)
    defence = get_defence(u1, u2, attack, action)
    
    return rolls[1] <= defence
    

def get_defence(a, d, attack, action):
    
    defence = d.defence
    
    defence += d.dcounters
    
    if a.type in d.dbonus:
        defence += d.dbonus[a.type]

    if hasattr(d, "improved_weapons"):
        defence += 1
  
    if attack < 1:
        defence = d.defence + attack -1
    
    if hasattr(d, "sabotaged"):
        defence = 0
    
    return defence


def get_attack(a, d, action):
    
    attack = a.attack
    
    attack -= a.acounters
    
    if hasattr(a, "is_crusading"):
        attack -= 1
    
    if hasattr(action, "lancing"):
        attack -= 2
    
    if hasattr(action, "high_morale"):
        attack -= 2

    if hasattr(a, "improved_weapons"):
        attack -= 3
 
    if d.type in a.abonus:
        attack -= a.abonus[d.type]
    
    return attack