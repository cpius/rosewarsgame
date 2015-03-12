import sys
from controller import Controller
from common import *
import random
import pygame
import view
from viewcommon import *
from view import View


def pause():
    while True:
        event = pygame.event.wait()

        if event.type == QUIT:
            exit_game()

        elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            return


def exit_game():
    sys.exit()


def menu_choice(view, menu):

    view.screen.fill(Color.Light_grey)
    for i, item in enumerate(menu):
        write(view.screen, item, view.interface.opponent_menu[i], view.interface.fonts["normal"])
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

        keys = {K_1: 1, K_2: 2, K_3: 3, K_4: 4}
        for key, item in keys.items():
            if event.type == KEYDOWN and event.key == key:
                return item


def figure_out_player_profile(view):
    profile = get_setting("profile")

    if profile:
        return profile
    else:
        view.screen.fill(Color.Light_grey)
        message = "Add a line to you settings.txt saying: 'profile: profile_name'"
        write(view.screen, message, view.interface.opponent_menu[0], view.interface.fonts["normal"])
        view.refresh()
        pause()
        return "quit"


def decide_opponent(view):
    menu = [str(i) + ". " + opponent_descriptions[Opponent(i).name] for i in range(1, 5)]
    return menu_choice(view, menu)


if __name__ == '__main__':

    view = View()
    opponent_choice = decide_opponent(view)

    controller = None
    if Opponent(opponent_choice) == Opponent.Internet:
        player_profile = figure_out_player_profile(view)
        if not player_profile == "quit":
            controller = Controller.from_network(player_profile)
    elif Opponent(opponent_choice) == Opponent.Load:
        controller = Controller.from_replay()
    elif Opponent(opponent_choice) == Opponent.HotSeat:
        controller = Controller.new_game("Human", "Human")
    elif Opponent(opponent_choice) == Opponent.AI:
        coinflip = random.randint(0, 1)
        if coinflip == 0:
            controller = Controller.new_game("Human", "AI")
        else:
            controller = Controller.new_game("AI", "Human")

    if controller:
        controller.run_game()
