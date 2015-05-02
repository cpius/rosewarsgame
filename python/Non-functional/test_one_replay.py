import json
from game import Game


testcase_file = "replay/20150320-165723/3.json"
replay_document = json.loads(open(testcase_file).read())
replay_game = Game.from_log_document(replay_document)

gamestate_document = replay_game.gamestate.to_document()

result, message = common.assert_equal_documents("one_replay", replay_document["gamestate"], gamestate_document, testcase_file)

print("The result was:", result)

if result:
    print("Everying is swell")
    print(message)
else:
    print("Ooohh it's in the rough!")
    print(message)
