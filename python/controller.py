import os
import sys
import glob
import json
import game.setup as setup
from gamestate.gamestate_module import Gamestate
from game.player import Player
from game.client import Client
from game.game_module import Game
from gamestate.outcome import Outcome
from view.view_module import View
from game.sound import Sound
from gamestate.gamestate_library import *
from view.view_control_library import *
import pygame
from game.settings import *


class Controller(object):
    def __init__(self, view, sound):
        self.view = view
        self.game = None
        self.sound = sound
        self.client = None
        self.positions = {}

    @property
    def selected_unit(self):
        return self.game.gamestate.all_units()[self.start_at] if self.start_at else None

    @property
    def start_at(self):
        return self.positions["start_at"] if "start_at" in self.positions else None

    CHECK_FOR_NETWORK_ACTIONS_EVENT_ID = pygame.USEREVENT + 1

    @classmethod
    def new_game(cls, green_intelligence, red_intelligence):
        if not os.path.exists("./replay"):
            os.makedirs("./replay")

        controller = Controller(View(), Sound())
        players = [Player("Green", green_intelligence), Player("Red", red_intelligence)]
        player1_units, player2_units = setup.get_start_units()
        gamestate = Gamestate(player1_units, player2_units, 1)
        controller.game = Game(players, gamestate)
        controller.game.gamestate.initialize_turn()
        controller.game.gamestate.actions_remaining = 1
        controller.clear_move()

        if play_fanfare:
            controller.sound.play_fanfare()

        return controller

    @classmethod
    def from_network(cls, player):

        client = Client(player)
        game_document = client.get_game()

        controller = cls(View(), Sound())
        controller.game = Game.from_log_document(game_document, player, True)
        controller.client = client
        player = controller.game.current_player()
        print("current player is", player.color, player.intelligence, player.profile)
        controller.clear_move()

        if play_fanfare:
            controller.sound.play_fanfare()

        return controller

    @classmethod
    def from_replay(cls, savegame_file=None):

        if not savegame_file:
            savegame_file = max(glob.iglob('./replay/*/*.json'), key=os.path.getctime)

        controller = cls(View(), Sound())
        savegame_document = json.loads(open(savegame_file).read())
        controller.game = Game.from_log_document(savegame_document)
        controller.clear_move()

        if controller.game.is_turn_done():
            controller.game.shift_turn()
        controller.game.gamestate.set_available_actions()

        player = controller.game.current_player()
        print("current player is", player.color, player.intelligence)

        if play_fanfare:
            controller.sound.play_fanfare()

        return controller

    def trigger_network_player(self):
        interval_in_milliseconds = 1000
        pygame.time.set_timer(self.CHECK_FOR_NETWORK_ACTIONS_EVENT_ID, interval_in_milliseconds)

        action, outcome, upgrade = self.client.select_action(self.game.gamestate)

        if action is None:
            return

        print("received action from network: ", action)
        if outcome:
            print("with outcome: ", outcome)
        if upgrade:
            print("with upgrade: ", upgrade)

        self.perform_action(action, outcome, upgrade)

        if self.game.is_player_human():
            # The turn changed. Stop listening for network actions
            pygame.time.set_timer(self.CHECK_FOR_NETWORK_ACTIONS_EVENT_ID, 0)
            if play_fanfare:
                self.sound.play_fanfare()

    def trigger_artificial_intelligence(self):

        action = self.game.current_player().ai.select_action(self.game)

        if action:
            self.perform_action(action)
        else:
            self.game.shift_turn()
            self.draw_game()

        if self.game.gamestate.is_extra_action():
            extra_action = self.game.current_player().ai.select_action(self.game)
            self.perform_action(extra_action)

    def run_game(self):

        self.game.gamestate.set_available_actions()

        self.draw_game(redraw_log=True)

        if self.game.is_player_network():
            self.trigger_network_player()

        if self.game.is_player_ai():
            self.trigger_artificial_intelligence()

        while True:
            event = pygame.event.wait()

            if event.type == self.CHECK_FOR_NETWORK_ACTIONS_EVENT_ID:
                self.trigger_network_player()

            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_item = self.view.get_item_from_mouse_click(event.pos)
                if clicked_item == Item.Help:
                    pass
                elif clicked_item == Item.Pass_action:
                    self.game.gamestate.pass_extra_action()
                    if self.game.gamestate.is_turn_done():
                        self.game.shift_turn()
                    self.clear_move()
                    self.game.gamestate.set_available_actions()
                    self.draw_game(redraw_log=True)
                else:
                    position = self.view.get_position_from_mouse_click(event.pos)
                    if not self.game.is_player_human():
                        position = position.flip()

                    if event.button == 1:
                        if self.game.is_player_human():
                            self.left_click(position)
                        else:
                            self.draw_game(redraw_log=True)
                    elif event.button == 3:
                        self.right_click(position)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and self.game.is_player_human():
                self.clear_move()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                print("positions:", self.positions)
                print(self.game.gamestate)

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                print(self.game.gamestate.available_actions)

            elif quit_game_requested(event):
                self.exit_game()

            self.view.refresh()

    def left_click(self, position):
        """
        :param position: The position of the left click
        :return: None
        Selects units or carries out actions if one is identified.
        """
        # Introduce variables
        gamestate = self.game.gamestate
        actions = gamestate.get_actions_with_move_with_attack_as_none()

        # Clear greyed out tiles
        self.draw_game(redraw_log=True)

        # If it's during an extra action, only tiles that indicate possible actions are clickable. If one of those are
        # clicked, perform that action.
        if gamestate.is_extra_action():
            if position in gamestate.enemy_units:
                actions = filter_actions(actions, {"start_at": self.start_at, "target_at": position})
            else:
                actions = filter_actions(actions, {"start_at": self.start_at, "end_at": position, "target_at": None})
            if actions:
                self.perform_action(actions[0])
            return

        # If start_at is not set, and a friendly_unit that can take an action is clicked, choose that as start_at.
        if not self.start_at:
            if position in gamestate.player_units:
                if filter_actions(actions, {"start_at": position}):
                    self.positions["start_at"] = position
                    self.draw_game()
            return

        # If the selected Unit is clicked again, deselect it.
        if self.start_at == position:
            self.clear_move()
            return

        # In the following a unit is selected and its not an extra action. If an action is indicated it is performed.
        if position in self.game.gamestate.all_units():
            criteria = {
                "start_at": self.start_at,
                "target_at": position
            }
        else:
            criteria = {
                "start_at": self.start_at,
                "end_at": position,
                "target_at": None
            }
        possible_actions = filter_actions(actions, criteria)

        # If the click doesnt indicate a possible action, deselect the unit.
        if not possible_actions:
            self.clear_move()
            return

        # If there is exactly one action, perform that action.
        if len(possible_actions) == 1:
            self.perform_action(possible_actions[0])

        # If more than one action is possible, get user feedback to specify which action should be performed.
        else:
            self.draw_game()
            unit = self.selected_unit

            # If the unit is melee, the user may need to specify an end_at.
            if unit.is_melee:
                end_at = self.pick_end_at(possible_actions)
                if end_at:
                    action, = (action for action in possible_actions if action.end_at == end_at)
                    self.perform_action(action)

            # If the unit is a specialist, the user may need to specify an ability.
            if unit.type is Type.Specialist:
                ability = self.pick_ability(unit)
                if ability:
                    action, = (action for action in possible_actions if action.ability == ability)
                    self.perform_action(action)

        # If after the action, there is an extra action, shade the board appropriately.
        if gamestate.is_extra_action():
            actions = gamestate.get_actions()
            if actions:
                self.positions["start_at"] = next(iter(actions)).start_at
                self.draw_game()

    def get_choice(self, keyevents, mouseevents):
        while True:
            event = pygame.event.wait()

            if event.type == pygame.KEYDOWN:
                if event.key in keyevents:
                    return keyevents[event.key]

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for mouse_click_position, result in mouseevents:
                    if within(event.pos, mouse_click_position):
                        return result

            elif quit_game_requested(event):
                self.exit_game()

    def get_choice_position(self, mouseevents):
        while True:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = self.view.get_position_from_mouse_click(event.pos)
                if position in mouseevents:
                    return mouseevents[position]

            elif quit_game_requested(event):
                self.exit_game()

    def pick_end_at(self, actions):
        end_ats = {action.end_at for action in actions}
        self.draw_game(shade_positions=end_ats)
        return self.get_choice_position({position: position for position in end_ats})

    def pick_upgrade(self, unit):
        self.view.draw_upgrade_options(unit)
        buttons = {pygame.K_1: 0, pygame.K_2: 1}
        areas = [[self.view.interface.upgrade_1_area, 0], [self.view.interface.upgrade_2_area, 1]]
        choice = self.get_choice(buttons, areas)
        return unit.get_upgrade(choice)

    def pick_ability(self, unit):
        self.view.draw_ask_about_ability(unit)
        choice = self.get_choice({pygame.K_1: 0, pygame.K_2: 1}, [])
        return unit.abilities[choice]

    def ask_about_move_with_attack(self, action):
        self.view.draw_ask_about_move_with_attack(action.end_at, action.target_at)
        return self.get_choice_position({action.target_at: True, action.end_at: False})

    def clear_move(self):
        self.positions = {}
        self.draw_game()

    def upgrade_should_be_performed(self, action):
        is_player_network = self.game.is_player_network()
        unit_has_extra_action = action.unit.has(State.extra_action)
        unit_should_be_upgraded = action.unit.should_be_upgraded()

        return unit_should_be_upgraded and not unit_has_extra_action and not is_player_network

    def perform_upgrade(self, action, upgrade):

        if upgrade is None:
            if self.game.is_player_human():
                upgrade = self.pick_upgrade(action.unit)
            else:
                choice = self.game.current_player().ai.select_upgrade(self.game)
                upgrade = action.unit.get_upgrade(choice)

        position = action.end_at if action.end_at in self.game.gamestate.player_units else action.target_at
        self.game.gamestate.player_units[position] = action.unit.get_upgraded_unit_from_upgrade(upgrade)

        string_upgrade = get_string_attributes(upgrade)
        self.game.save_option("upgrade", string_upgrade)

        if self.game.is_enemy_network():
            self.client.send_upgrade_choice(string_upgrade, self.game.gamestate.action_count)

    def perform_move_with_attack(self, action, outcome):
        self.draw_game(redraw_log=True)
        move_with_attack = self.ask_about_move_with_attack(action)

        self.game.save_option("move_with_attack", move_with_attack)
        if self.game.is_enemy_network():
            self.client.send_move_with_attack(move_with_attack, self.game.gamestate.action_count)

        if move_with_attack:
            self.view.draw_post_movement(action)
            self.game.gamestate.move_melee_unit_to_target_tile(action)

        self.game.gamestate.set_available_actions()

    def move_with_attack_should_be_performed(self, action, outcome):
        is_mwa_possible = self.game.gamestate.is_post_move_with_attack_possible(action, outcome)

        return action.move_with_attack is None and is_mwa_possible

    def determine_outcome(self, action):
        if self.game.is_enemy_network():
            return self.client.send_action(action.to_network(self.game.gamestate.action_count))
        else:
            return Outcome.determine_outcome(action, self.game.gamestate)

    def perform_action(self, action, outcome=None, upgrade=None):
        self.draw_game()

        if not outcome:
            outcome = self.determine_outcome(action)

        self.view.draw_action(action, self.game)
        self.game.do_action(action, outcome)

        if play_action_sounds:
            self.sound.play_action(action)

        animation_delay = pause_for_animation
        if action.is_attack:
            animation_delay = pause_for_animation_attack
        pygame.time.delay(animation_delay)
        self.draw_game()

        if self.move_with_attack_should_be_performed(action, outcome):
            self.perform_move_with_attack(action, outcome)

        if self.game.gamestate.is_ended():
            self.game_end()

        if self.upgrade_should_be_performed(action):
            self.perform_upgrade(action, upgrade)

        if self.game.is_turn_done():
            self.game.shift_turn()

        self.draw_game(redraw_log=True)

        if not self.game.gamestate.is_extra_action():
            self.clear_move()

        self.game.save(self.view, action, outcome)

        if verbose:
            print("Action performed. Expecting action from", self.game.current_player().intelligence)

        if self.game.is_player_human():
            return
        elif self.game.is_player_network():
            expected_action_number = self.game.gamestate.action_count + 1
            print("Waiting for network action from network with number", expected_action_number)
            self.trigger_network_player()
        else:
            self.trigger_artificial_intelligence()

    def draw_game(self, redraw_log=False, shade_actions=True, shade_positions=None):
        if shade_actions and "start_at" in self.positions:
            actions = self.game.gamestate.get_actions(self.positions)
        else:
            actions = None
        self.view.draw_game(self.game, actions, shade_positions, redraw_log)

    def pause(self):
        while True:
            event = pygame.event.wait()
            if quit_game_requested(event):
                self.exit_game()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

    @staticmethod
    def exit_game():
        sys.exit()

    def game_end(self):
        self.view.draw_game_end(self.game.current_player().color, self.game)
        self.pause()
        self.exit_game()

    def right_click(self, position):
        """
        :param position: The position that is right clicked
        :return: None
        Shows the details of the unit being right clicked. If a friendly unit is selected and it can
        perform an action on the right clicked position, show info for this action.
        """
        self.draw_game()

        if position not in self.game.gamestate.all_units():
            self.clear_move()
            return

        self.view.show_unit_zoomed(self.game.gamestate.all_units()[position])

        if self.start_at:
            actions = self.game.gamestate.get_actions(
                {"start_at": self.start_at, "target_at": position})
            if actions:
                self.draw_game(shade_actions=actions)
                self.view.show_battle_hint(self.game.gamestate, self.start_at, position)
            self.positions = {}
