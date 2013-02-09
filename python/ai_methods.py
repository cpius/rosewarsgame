from __future__ import division
import battle



def document_actions(ai_type, actions, p):
    
    if p[0].actions == 2:
        taction = "1"
    else:
        taction = "2"
        
    if p[0].second_action:
        taction += ".2"
        
    out = open(p[0].color + " AI actions " + taction + ".txt", 'w')
    
    out.write("ACTIONS:\n\n")
    for action in actions:
        out.write(str(action) + "\n")
        if action.is_attack:
            a = p[0].units[action.startpos]
            d = p[1].units[action.attackpos]
            out.write("Base attack: " +  str(a.attack) + "\n")
            out.write("Attack Counters: " +  str(a.acounters) + "\n")
            out.write("Defence Counters: " +  str(d.dcounters) + "\n")
            if hasattr(action, "abonus"):
                out.write("Attack Move Bonus: " +  str(action.abonus) + "\n")
            attack = battle.get_attack(a,d, action)
            defence = battle.get_defence(a,d, attack, action)
            out.write("Defender: " + d.name + ", A: " + str(attack) + " D: " + str(defence)  + "\n\n")
            if action.sub_actions:
                out.write("Sub actions:\n")
                for i, sub_action in enumerate(action.sub_actions):
                    out.write("Sub action " + str(i +1) + "\n")
                    a = p[0].units[sub_action.startpos]
                    d = p[1].units[sub_action.attackpos]
                    out.write("Base attack: " +  str(a.attack) + "\n")
                    out.write("Attack Counters: " +  str(a.acounters) + "\n")
                    out.write("Defence Counters: " +  str(d.dcounters) + "\n")
                    if hasattr(sub_action, "abonus"):
                        out.write("Attack Move Bonus: " +  str(sub_action.abonus) + "\n")
                    attack = battle.get_attack(a,d, sub_action)
                    defence = battle.get_defence(a,d, attack, sub_action)
                    out.write("Defender: " + d.name + ", A: " + str(attack) + " D: " + str(defence)  + "\n\n")        
                        
        out.write("Score: " + str(round(action.score,2)) + "\n\n")
    
    out.close()




def chance_of_win(a, d, action):

    attack = battle.get_attack(a, d, action)
    defence = battle.get_defence(a, d, attack, action)

    if attack < 0:
        attack = 0
    
    if attack > 6:
        attack = 6
        
    if defence < 0:
        defence = 0
    
    if defence > 6:
        defence = 6

    return ((7 - attack) / 6) * ((6 - defence) / 6)