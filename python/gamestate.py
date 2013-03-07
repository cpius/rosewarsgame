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


def save_gamestate(p):
    
    gamestate = []

    for i in range(2):
        gamestate.append([p[i].color, p[i].ai_name, p[i].actions_remaining, hasattr(p[i], "extra_action")])
        
        unit_states = []
        for pos, unit in p[i].units.items():
            unit_state = unit.__dict__
            unit_state["pos"] = pos
            unit_state["name"] = unit.name
            unit_states.append(unit_state)
        
        gamestate.append(unit_states)
        
    return gamestate



def load_gamestate(gamestate):
    p = []
    
    for i in range(2):
        
        player = setup.Player(gamestate[i * 2][0])
        player.ai_name = gamestate[i * 2][1]
        player.actions_remaining = gamestate[i * 2][2]
        if gamestate[i * 2][3]:
            player.extra_action = True
    
        load_units = {}
        for unit in gamestate[i * 2 + 1]:
            load_units[unit['pos']] = getattr(units_module, unit['name'].replace(" ", "_"))()
            for key, item in unit.items():
                setattr(load_units[unit['pos']], key, item)

        player.units = load_units
        p.append(player)
    
    return p
    


def copy_p(p):
    
    gamestate = save_gamestate(p)
    return load_gamestate(gamestate)


def save_action(action):
    
    action_state = [{}]
    
    for key, item in action.__dict__.items():
        if key != "sub_actions":
            action_state[0][key] = item
        
    for sub_action in action.sub_actions:
        action_state.append({})
        for key, item in sub_action.__dict__.items():
            action_state[-1][key] = item
            
    return action_state


def write_gamestate(p, path):

    out = open(path, 'w')

    for i in range(2):
        out.write(p[i].color + "\n")
        out.write("Player: " + p[i].ai_name + "\n")
        out.write("Actions Remaining: " + str(p[i].actions_remaining) + "\n")
        out.write("Extra Action: " + str(hasattr(p[i], "extra_action")) + "\n")
        out.write("\n")
        out.write("Units\n")
        for pos, unit in p[i].units.items():
            out.write(unit.name + ":" + "(" + str(pos[0]) + "," + str(pos[1]) + ")" + "\n")
            out.write(str(unit.__dict__) + "\n\n")

        out.write("\n")
    out.close()


def read_gamestate(path):
    inp = open(path)

    p = []

    for i in range(2):
        color = inp.readline().rstrip("\n")
        player = setup.Player(color)
        player.ai_name = inp.readline().split()[1].rstrip("\n")
        player.actions_remaining = int(inp.readline().split()[2].rstrip("\n"))
        if inp.readline().split()[2].rstrip("\n") == "True":
            player.extra_action = True
        inp.readline()
        inp.readline()
        line = inp.readline()
        player.units = {}
        while line != "\n":
            line = line.split(":")
            name = line[0]
            pos = eval(line[1].rstrip("\n"))
            player.units[pos] = getattr(units_module, name.replace(" ", "_"))()
            d = eval(inp.readline())
            for key, item in d.items():
                setattr(player.units[pos], key, item)
            inp.readline()
            line = inp.readline()

        p.append(player)

    return p



def load_action(action_state):

    action = mover.Action(action_state[0]["unit"], action_state[0]["startpos"], action_state[0]["endpos"], action_state[0]["attackpos"], action_state[0]["is_attack"], action_state[0]["move_with_attack"], action_state[0]["is_ability"], action_state[0]["ability"])
    
    for key, item in action_state[0].items():
        if key not in start_attributes_actions:
            setattr(action, key, item)
    
    if len(action_state) > 1:
        action.sub_actions = []
        for i in range(1, len(action_state)):
            action.sub_actions.append(mover.Action(action_state[i]["unit"], action_state[i]["startpos"], action_state[i]["endpos"], action_state[i]["attackpos"], action_state[i]["is_attack"], action_state[i]["move_with_attack"], action_state[i]["is_ability"], action_state[i]["ability"]))
            for key, item in action_state[i].items():
                if key not in start_attributes_actions:
                    setattr(action.sub_actions[-1], key, item)

    return action
    
    
def copy_action(action):
    
    action_state = save_action(action)
    return load_action(action_state)