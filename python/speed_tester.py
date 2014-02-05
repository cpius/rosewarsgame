import profile
import gamestate
import json
from gamestate import Gamestate
from player import Player
from game import Game


games = []
for path in ["./replay/20140202-213819/2.json", "./replay/20140202-212231/1.json", "./replay/20140203-004236/1.json"]:
    document = json.loads(open(path).read())
    gamestate = Gamestate.from_document(document["gamestate"])
    gamestate.set_actions_remaining(2)
    gamestate.set_available_actions()
    players = [Player("Green", "AI"), Player("Red", "AI")]
    games.append(Game(players, gamestate))


def a():
    for game in games:
        game.current_player().ai.select_action(game)


profile.run('a()')

