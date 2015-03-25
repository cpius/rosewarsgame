import sys
import setup
from gamestate import Gamestate
import os
import glob
import interface_settings  # Present to avoid circular import
from player import Player
from client import Client
from game import Game
from outcome import Outcome
import json
from view import View
from sound import Sound
from common import get_setting
from viewcommon import (USEREVENT, KEYDOWN, QUIT, K_ESCAPE, KMOD_LMETA, KMOD_RMETA, K_a, K_g, K_q, K_1, K_2, pygame,
                        Type, State, within, get_string_upgrade)


class Controller(object):
    def __init__(self, view, sound):
        self.view = view
        self.game = None
        self.sound = sound
        self.client = None
        self.positions = {"start_at": None, "end_at": None}

    @property
    def selected_unit(self):
        return self.game.gamestate.all_units()[self.start_at] if self.start_at else None

    @property
    def start_at(self):
        return self.positions["start_at"]

    @property
    def has_start_at(self):
        return self.start_at is not None

    def set_start_at(self, start_at):
        self.positions["start_at"] = start_at

    CHECK_FOR_NETWORK_ACTIONS_EVENT_ID = USEREVENT + 1

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

        if get_setting("play_fanfare"):
            controller.sound.play_fanfare()

        return controller

    @classmethod
    def from_network(cls, player):

        client = Client(player)
        game_document = client.get_game()

        controller = cls(View())
        controller.game = Game.from_log_document(game_document, player, True)
        controller.client = client
        player = controller.game.current_player()
        print("current player is", player.color, player.intelligence, player.profile)
        controller.clear_move()

        if get_setting("play_fanfare"):
            controller.sound.play_fanfare()

        return controller

    @classmethod
    def from_replay(cls, savegame_file=None):

        if not savegame_file:
            savegame_file = max(glob.iglob('./replay/*/*.json'), key=os.path.getctime)

        controller = cls(View())
        savegame_document = json.loads(open(savegame_file).read())
        controller.game = Game.from_log_document(savegame_document)
        controller.clear_move()

        if controller.game.is_turn_done():
            controller.game.shift_turn()

        player = controller.game.current_player()
        print("current player is", player.color, player.intelligence)

        if get_setting("play_fanfare"):
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
            if get_setting("play_fanfare"):
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
                position = self.view.get_position_from_mouse_click(event.pos)
                if not self.game.is_player_human():
                    position = position.flip()

                if event.button == 1:
                    if self.game.is_player_human():
                        self.left_click(position)
                elif event.button == 3:
                    self.right_click(position)

            if event.type == KEYDOWN and event.key == K_ESCAPE and self.game.is_player_human():
                self.clear_move()

            elif event.type == KEYDOWN and event.key == K_g:
                print(self.game.gamestate)

            elif event.type == KEYDOWN and event.key == K_a:
                print(self.game.gamestate.available_actions)

            elif self.quit_game_requested(event):
                self.exit_game()

            self.view.refresh()

    def left_click(self, position):
        """
        :param position: The position of the left click
        :return: None
        Selects units or carries out actions if one is identified.
        """

        # Clear greyed out tiles
        self.draw_game(redraw_log=True)


        # If the Unit is clicked again, deselect the unit.
        if self.start_at == position:
            if self.game.gamestate.is_extra_action():
                self.game.gamestate.player_units[position].remove(State.movement_remaining)
                self.game.gamestate.player_units[position].remove(State.extra_action)
                if self.game.is_turn_done():
                    self.game.shift_turn()
                self.game.gamestate.set_available_actions()

            self.draw_game(redraw_log=True)

            self.clear_move()
            return

        # If start_at is not set, and a suitable start_at is chosen, set start_at.
        if not self.start_at and position in self.game.gamestate.player_units:
            possible_actions = self.game.gamestate.get_actions({"start_at": position})
            if possible_actions:
                self.set_start_at(position)
                self.view.draw_game(self.game, position, possible_actions, True)
                return

        # Determine possible actions
        if position in self.game.gamestate.all_units():
            criteria = {
                "start_at": self.start_at,
                "target_at": position
            }
            possible_actions = self.game.gamestate.get_actions_with_move_with_attack_as_none(criteria)
        else:
            criteria = {
                "start_at": self.start_at,
                "end_at": position,
                "target_at": None
            }
            possible_actions = self.game.gamestate.get_actions(criteria)

        # If there are no possible actions, deselect the unit.
        if not possible_actions:
            self.clear_move()
            return

        # If there is exactly one action, perform that action.
        if len(possible_actions) == 1:
            self.perform_action(possible_actions[0])

        # If more than one action is possible, get user feedback to specify which action should be performed.
        else:
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

        if self.game.gamestate.is_extra_action():
            actions = self.game.gamestate.get_actions()
            if actions:
                self.positions["start_at"] = actions[0].start_at
                self.view.draw_game(self.game, actions[0].start_at, actions, False)

    def get_choice(self, keyevents, mouseevents):
        while True:
            event = pygame.event.wait()

            if event.type == KEYDOWN:
                if event.key in keyevents:
                    return keyevents[event.key]

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for mouse_click_position, result in mouseevents:
                    if within(event.pos, mouse_click_position):
                        return result

            elif self.quit_game_requested(event):
                self.exit_game()

    def get_choice_position(self, mouseevents):
        while True:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                position = self.view.get_position_from_mouse_click(event.pos)
                if position in mouseevents:
                    return mouseevents[position]

            elif self.quit_game_requested(event):
                self.exit_game()

    def pick_end_at(self, actions):
        end_ats = [action.end_at for action in actions]
        self.view.shade_positions(end_ats)
        return self.get_choice_position({position: position for position in end_ats})

    def pick_upgrade(self, unit):
        self.view.draw_upgrade_options(unit)
        buttons = {K_1: 0, K_2: 1}
        areas = [[self.view.interface.upgrade_1_area, 0], [self.view.interface.upgrade_2_area, 1]]
        choice = self.get_choice(buttons, areas)

        return unit.get_upgrade(choice)

    def pick_ability(self, unit):
        self.view.draw_ask_about_ability(unit)
        choice = self.get_choice({K_1: 0, K_2: 1}, [])
        return unit.abilities[choice]

    def ask_about_move_with_attack(self, action):
        self.view.draw_ask_about_move_with_attack(action.end_at, action.target_at)

        return self.get_choice_position({action.target_at: True, action.end_at: False})

    def clear_move(self):
        self.positions = {"start_at": None, "end_at": None}
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

        string_upgrade = get_string_upgrade(upgrade)
        self.game.save_option("upgrade", string_upgrade)

        if self.game.is_enemy_network():
            self.client.send_upgrade_choice(string_upgrade, self.game.gamestate.action_count)

    def perform_move_with_attack(self, action, outcome):
        move_with_attack = self.ask_about_move_with_attack(action)

        self.draw_game(redraw_log=True)

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

        self.view.draw_action(action, self.game.logbook, not self.game.is_player_human())
        self.game.do_action(action, outcome)

        if get_setting("play_action_sounds"):
            self.sound.play_action(action)

        animation_delay = interface_settings.pause_for_animation
        if action.is_attack:
            animation_delay = interface_settings.pause_for_animation_attack
        pygame.time.delay(animation_delay)
        self.draw_game()

        if self.move_with_attack_should_be_performed(action, outcome):
            self.perform_move_with_attack(action, outcome)

        if self.game.gamestate.is_ended():
            self.game_end()

        if self.upgrade_should_be_performed(action):
            self.perform_upgrade(action, upgrade)

        self.game.save(self.view, action, outcome)

        if self.game.is_turn_done():
            self.game.shift_turn()

        self.draw_game(redraw_log=True)

        if not self.game.gamestate.is_extra_action():
            self.clear_move()
            action.unit.remove(State.movement_remaining)

        action.unit.remove_states_with_value_zero()

        print("Action performed. Expecting action from", self.game.current_player().intelligence)

        if self.game.is_player_human():
            return
        elif self.game.is_player_network():
            expected_action_number = self.game.gamestate.action_count + 1
            print("Waiting for network action from network with number", expected_action_number)
            self.trigger_network_player()
        else:
            self.trigger_artificial_intelligence()

    def draw_game(self, redraw_log=False):
        self.view.draw_game(self.game, redraw_log=redraw_log)

    def pause(self):
        while True:
            event = pygame.event.wait()
            if self.quit_game_requested(event):
                self.exit_game()
            elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

    def quit_game_requested(self, event):
        return event.type == QUIT or (event.type == KEYDOWN and self.command_q_down(event.key))

    @staticmethod
    def command_q_down(key):
        is_meta = pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA
        return key == K_q and is_meta

    @staticmethod
    def escape(event):
        return event.type == KEYDOWN and event.key == K_ESCAPE

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
                self.view.shade_actions(actions)
                self.view.show_battle_hint(self.game.gamestate, self.start_at, position)
            self.positions = {"start_at": None, "end_at": None}
