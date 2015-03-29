import json
from gamestate.gamestate_module import Gamestate
from time import time
from gamestate import action_getter


def run():
    path = "./../Version_1.0/Tests/General/Action_1.json"
    document = json.loads(open(path).read())
    gamestate = Gamestate.from_document(document["gamestate"])

    nloops = 100
    total_time = 0
    for _ in range(nloops):
        t = time()
        action_getter.get_actions(gamestate)
        total_time += time() - t

    print("Time used to find all actions", str(nloops), "times:", str(round(total_time, 3)))