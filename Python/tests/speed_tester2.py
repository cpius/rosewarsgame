import profile
import gamestate
import json
from gamestate import Gamestate
from player import Player
from game import Game
from common import Intelligence
from glob import glob


games = []
for path in glob("./keep_replays/*.json"):
    document = json.loads(open(path).read())
    gamestate = Gamestate.from_document(document["gamestate"])
    gamestate.actions_remaining = 2
    gamestate.set_available_actions()
    players = [Player("Green", Intelligence.AI), Player("Red", Intelligence.AI)]
    games.append(Game(players, gamestate))


def a():
    for game in games:
        game.current_player().ai.select_action(game)


profile.run('a()')

