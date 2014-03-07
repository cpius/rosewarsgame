import sys
from controller import Controller
from common import *
import random
import pygame
import view
from viewcommon import *
from view import View


def menu_choice(view, menu):

    view.screen.fill(colors["light_grey"])
    for i, item in enumerate(menu):
        write(view.screen, item, view.interface.help_menu[i], view.interface.fonts["normal"])
    view.refresh()

    while 1:
        event = pygame.event.wait()

        if quit_game_requested(event):
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if within(event.pos, view.interface.help_area):
                return "quit"

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(menu)):
                if within(event.pos, view.interface.opponent_menu[i]):
                    return i + 1


def figure_out_player_profile():
    profile = get_setting("profile")

    if profile:
        return profile
    else:
        print "Please specify a profile name\n> ",
        profile = sys.stdin.readline().rstrip()
        with open("settings_user.py", "a") as settings_user_file:
            settings_user_file.write("profile = \"" + profile + "\"\r\n")

        return figure_out_player_profile()


def decide_opponent(view):
    menu = [opponent_descriptions[Opponent.name[i]] for i in range(1, 5)]
    return menu_choice(view, menu)


if __name__ == '__main__':

    view = View()
    opponent_choice = decide_opponent(view)

    controller = None
    if opponent_choice == Opponent.Internet:
        player_profile = figure_out_player_profile()
        controller = Controller.from_network(player_profile)
    elif opponent_choice == Opponent.Load:
        controller = Controller.from_replay(sys.argv[1])
    elif opponent_choice == Opponent.HotSeat:
        controller = Controller.new_game("Human", "Human")
    elif opponent_choice == Opponent.AI:
        coinflip = random.randint(0, 1)
        if coinflip == 0:
            controller = Controller.new_game("Human", "AI")
        else:
            controller = Controller.new_game("AI", "Human")

    if controller:
        controller.run_game()

