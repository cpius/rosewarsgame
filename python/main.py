import sys
from controller import Controller
import imp
from common import *
import random


def figure_out_player_profile():
    filename, pathname, description = imp.find_module("settings_user")
    settings_user = imp.load_module("settings_user", filename, pathname, description)

    profile = None
    if hasattr(settings_user, "profile"):
        profile = settings_user.profile

    filename.close()

    if profile:
        return profile
    else:
        print "Please specify a profile name\n> ",
        profile = sys.stdin.readline().rstrip()
        with open("settings_user.py", "a") as settings_user_file:
            settings_user_file.write("profile = \"" + profile + "\"\r\n")

        return figure_out_player_profile()


def decide_opponent():
    global i, opponent_choice
    print "Choose an opponent"
    for i in range(1, 5):
        print str(i) + ":", opponent_descriptions[Opponent.name[i]]
    print "> ",
    return int(sys.stdin.readline().rstrip())


if __name__ == '__main__':

    opponent_choice = decide_opponent()

    controller = None
    if opponent_choice == Opponent.Internet:
        player_profile = figure_out_player_profile()
        controller = Controller.from_network(player_profile)
    elif opponent_choice == Opponent.Load:
        controller = Controller.from_replay(sys.argv[1])
    elif opponent_choice == Opponent.HotSeat:
        controller = Controller.new_game("Human", "Human")
    elif opponent_choice == Opponent.Advancer:
        coinflip = random.randint(0, 1)
        if coinflip == 0:
            controller = Controller.new_game("Human", Opponent.write[opponent_choice])
        else:
            controller = Controller.new_game(Opponent.write[opponent_choice], "Human")

    if controller:
        controller.run_game()
