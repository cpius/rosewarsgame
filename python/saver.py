import units as units_module
import setup
import ai_module
import gamestate_module
from action import Action

start_attributes_actions = ["unit", "startpos", "endpos", "attackpos", "is_attack", "move_with_attack",
                            "is_ability", "ability"]


def save_gamestate(g):
    
    gamestate = []

    for i in range(2):
        gamestate.append([g.players[i].color, g.players[i].ai_name, g.players[i].actions_remaining,
                          hasattr(g.players[i], "extra_action")])
        
        unit_states = []
        for pos, unit in g.units[i].items():
            unit_state = {"pos": pos, "name": unit.name}
            for key, item in unit.__dict__.items():
                unit_state[key] = item
            unit_states.append(unit_state)
        
        gamestate.append(unit_states)
        
    return gamestate


def load_gamestate(gamestate):

    players = []
    units = []

    for i in range(2):
        
        player = setup.Player(gamestate[i * 2][0])
        player.ai_name = gamestate[i * 2][1]
        if player.ai_name != "Human":
            player.ai = ai_module.AI(player.ai_name)
        player.actions_remaining = gamestate[i * 2][2]
        if gamestate[i * 2][3]:
            player.extra_action = True

        players.append(player)

        load_units = {}
        for unit in gamestate[i * 2 + 1]:
            load_units[unit['pos']] = getattr(units_module, unit['name'].replace(" ", "_"))()
            for key, item in unit.items():
                setattr(load_units[unit['pos']], key, item)

        units.append(load_units)

    g = gamestate_module.Gamestate(players[0], units[0], players[1], units[1])
    
    return g


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


def load_action(action_state):

    action = Action(action_state[0]["startpos"], action_state[0]["endpos"], action_state[0]["attackpos"], action_state[0]["is_attack"], action_state[0]["move_with_attack"], action_state[0]["is_ability"], action_state[0]["ability"])
    
    for key, item in action_state[0].items():
        if key not in start_attributes_actions:
            setattr(action, key, item)
    
    if len(action_state) > 1:
        action.sub_actions = []
        for i in range(1, len(action_state)):
            action.sub_actions.append(Action(action_state[i]["startpos"], action_state[i]["endpos"], action_state[i]["attackpos"], action_state[i]["is_attack"], action_state[i]["move_with_attack"], action_state[i]["is_ability"], action_state[i]["ability"]))
            for key, item in action_state[i].items():
                if key not in start_attributes_actions:
                    setattr(action.sub_actions[-1], key, item)

    return action
    
    
def copy_action(action):
    
    action_state = save_action(action)
    return load_action(action_state)


def copy_actions(actions):

    new_actions = []
    for action in actions:
        action_state = save_action(action)
        new_actions.append(load_action(action_state))

    return new_actions

