import units_module
import setup
import mover


start_attributes = ["zoc", "has_attack", "has_ability", "pic", "attack", "defence", "range", "movement","abonus","dbonus","type", "pos"]

start_attributes_actions = ["unit", "startpos", "endpos", "attackpos", "is_attack", "move_with_attack", "is_ability", "ability"]

def save_gamestate(p):
    
    gamestate = []
    
    for i in range(2):
        gamestate.append([p[i].color, p[i].ai, p[i].actions_remaining, hasattr(p[i], "extra_action")])
        
        unit_states = []
        for pos, unit in p[i].units.items():
            d = unit.__dict__
            unit_state = {}
            unit_state['pos'] = pos
            for key, item in d.items():
                if key not in start_attributes:
                    unit_state[key] = item
            unit_states.append(unit_state)
        
        gamestate.append(unit_states)
    
    return gamestate


def load_gamestate(gamestate):
    p = []
    
    for i in range(2):
        
        player = setup.Player(gamestate[i*2][0])
        player.ai = gamestate[i*2][1]
        player.actions_remaining = gamestate[i*2][2]
        if gamestate[i*2][3]:
            player.extra_action = True
    
        load_units = {}
        for unit in gamestate[ i*2 + 1]:
            load_units[unit['pos']] = getattr(units_module, unit['name'].replace(" ", "_"))(player.color)
            load_units[unit['pos']].used = False
            load_units[unit['pos']].xp_gained_this_round = False
            for key, item in unit.items():
                if key not in start_attributes:
                    setattr(load_units[unit['pos']], key, item)


        player.units = load_units
        p.append(player)
    
    return p
    


def copy_p(p):
    
    saved_gamestate = save_gamestate(p)
    return load_gamestate(saved_gamestate)



def save_actionstate(action):
    
    actionstate = [{}]
    
    for key, item in action.__dict__.items():
        if key != "sub_actions":
            actionstate[0][key] = item
        
    for sub_action in action.sub_actions:
        actionstate.append({})
        for key, item in sub_action.__dict__.items():
            actionstate[-1][key] = item
            
    return actionstate


def load_action(actionstate):

    action = mover.Action(actionstate[0]["unit"], actionstate[0]["startpos"], actionstate[0]["endpos"], actionstate[0]["attackpos"], actionstate[0]["is_attack"], actionstate[0]["move_with_attack"], actionstate[0]["is_ability"], actionstate[0]["ability"])
    
    for key, item in actionstate[0].items():
        if key not in start_attributes_actions:
            setattr(action, key, item)
    
    if len(actionstate) > 1:
        action.sub_actions = []
        for i in range(1, len(actionstate)):
            action.sub_actions.append(mover.Action(actionstate[i]["unit"], actionstate[i]["startpos"], actionstate[i]["endpos"], actionstate[i]["attackpos"], actionstate[i]["is_attack"], actionstate[i]["move_with_attack"], actionstate[i]["is_ability"], actionstate[i]["ability"]))
            for key, item in actionstate[i].items():
                if key not in start_attributes_actions:
                    setattr(action.sub_actions[-1], key, item)
            
    
    return action
    
    
def copy_action(action):
    
    actionstate = save_actionstate(action)
    return load_action(actionstate)