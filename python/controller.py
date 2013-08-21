from __future__ import division
import pygame
import sys
from pygame.locals import *
import setup
from gamestate import Gamestate
import os
import interface_settings as settings
from player import Player
from action import Action
from units import Unit
from client import Client
from game import Game
from outcome import Outcome
import json
from common import *


class Controller(object):
    def __init__(self, view):
        self.view = view
        self.game = None
        self.client = None

    CHECK_FOR_NETWORK_ACTIONS_EVENT_ID = USEREVENT + 1

    @classmethod
    def new_game(cls, view):
        if not os.path.exists("./replay"):
            os.makedirs("./replay")

        controller = Controller(view)

        players = [Player("Green", settings.player1_ai), Player("Red", settings.player2_ai)]

        player1_units, player2_units = setup.get_start_units()
        gamestate = Gamestate(player1_units, player2_units, 1)

        controller.game = Game(players, gamestate)

        controller.game.gamestate.initialize_turn()

        controller.game.gamestate.actions_remaining = 1

        controller.clear_move()

        return controller

    @classmethod
    def from_network(cls, view, game_id, player):
        controller = cls(view)

        controller.game_id = game_id
        controller.client = Client(game_id)
        controller.game = Game.from_log_document(controller.client.get_game(), player, True)

        player = controller.game.current_player()
        print "current player is", player.color, player.intelligence, player.profile
        controller.clear_move()

        return controller

    @classmethod
    def from_replay(cls, view, savegame_file):
        controller = cls(view)
        savegame_document = json.loads(open(savegame_file).read())
        controller.game = Game.from_log_document(savegame_document)
        controller.clear_move()

        return controller

    def trigger_network_player(self):
        interval_in_milliseconds = 1000
        pygame.time.set_timer(self.CHECK_FOR_NETWORK_ACTIONS_EVENT_ID, interval_in_milliseconds)

        action, outcome, upgrade = self.client.select_action(self.game.gamestate)

        if action is None:
            return

        print "received action from network: " + str(action)

        self.perform_action(action, outcome, upgrade)

        if self.game.is_player_human():
            # The turn changed. Stop listening for network actions
            pygame.time.set_timer(self.CHECK_FOR_NETWORK_ACTIONS_EVENT_ID, 0)

    def trigger_artificial_intelligence(self):

        action = self.game.current_player().ai.select_action(self.game)

        if action:
            self.perform_action(action)
        else:
            self.game.shift_turn()
            self.view.draw_game(self.game)

        if self.game.gamestate.is_extra_action():
            extra_action = self.game.current_player().ai.select_action(self.game.gamestate)
            self.perform_action(extra_action)

    def perform_extra_action(self, position):
        if position in self.game.gamestate.enemy_units:
            self.perform_melee_attack(position)
        elif position == self.start_at or position not in self.game.gamestate.player_units:
            self.perform_move(position)

    def perform_ability(self, position):
        if len(self.selected_unit.abilities) > 1:
            index = self.get_input_abilities(self.selected_unit)

            ability = self.selected_unit.abilities.keys()[index]
        else:
            ability = self.selected_unit.abilities.keys()[0]
        action = Action(self.game.gamestate.all_units(), self.start_at, target_at=position, ability=ability)
        if action in self.game.gamestate.get_actions():
            self.perform_action(action)
        else:
            self.clear_move()
            self.view.draw_game(self.game)

    def select_unit(self, position):
        self.start_at = position
        self.selected_unit = self.game.gamestate.player_units[self.start_at]
        illustrate_actions = [action for action in self.game.gamestate.get_actions() if action.start_at == position]
        self.view.draw_game(self.game, position, illustrate_actions)

    def perform_ranged_attack(self, position):
        action = Action(self.game.gamestate.all_units(), self.start_at, target_at=position)
        if action in self.game.gamestate.get_actions():
            self.perform_action(action)

    def perform_melee_attack(self, position):
        all_actions = self.game.gamestate.get_actions()

        matching_actions = [action for action in all_actions if self.is_same_start_and_target(action, position)]

        if not matching_actions:
            return

        if len(matching_actions) == 1:
            self.perform_action(matching_actions[0])
            return

        self.view.draw_game(self.game)

        if len(set([action.end_at for action in matching_actions])) > 1:
            matching_actions = self.pick_actions_end_position(matching_actions)

        if any(action.move_with_attack for action in matching_actions):
            # Human actions always start out with unknown move_with_attack (they are asked later)
            matching_actions[0].move_with_attack = None

        self.perform_action(matching_actions[0])

    def perform_move(self, position):
        action = Action(self.game.gamestate.all_units(), self.start_at, end_at=position)
        if action in self.game.gamestate.get_actions():
            self.perform_action(action)
        elif not self.selecting_extra_action():
            self.clear_move()
            self.view.draw_game(self.game)

    def left_click(self, position):
        if self.selecting_extra_action():
            self.perform_extra_action(position)

        elif self.selecting_ability_target(position):
            self.perform_ability(position)

        elif self.selecting_active_unit(position):
            self.select_unit(position)

        elif self.selecting_ranged_target(position):
            self.perform_ranged_attack(position)

        elif self.selecting_melee_target(position):
            self.perform_melee_attack(position)

        elif self.selecting_move(position):
            self.perform_move(position)

        elif self.start_at and self.start_at == position:
            self.clear_move()
            self.view.draw_game(self.game)

    def is_same_start_and_target(self, action, position):
        same_start = action.start_at == self.start_at
        same_target = action.target_at and action.target_at == position
        return same_start and same_target

    def pick_actions_end_position(self, actions):

        end_positions = [action.end_at for action in actions]

        self.view.shade_positions(end_positions)

        while True:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = self.view.get_position_from_mouse_click(event.pos)

                if event.button == 1:
                    matching_actions = [action for action in actions if action.end_at == position]
                    if matching_actions:
                        return matching_actions

            elif self.quit_game_requested(event):
                self.exit_game()

    def right_click(self, position):
        if not self.start_at:
            self.show_unit(position)
        else:
            if position in self.game.gamestate.enemy_units:
                self.show_attack(position)

    def clear_move(self):
        self.start_at = self.end_position = self.selected_unit = None

    def run_game(self):

        self.game.gamestate.set_available_actions()

        self.view.draw_game(self.game)

        if self.game.is_player_network():
            self.trigger_network_player()

        while True:
            event = pygame.event.wait()

            if event.type == self.CHECK_FOR_NETWORK_ACTIONS_EVENT_ID:
                self.trigger_network_player()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = self.view.get_position_from_mouse_click(event.pos)

                if event.button == 1 and self.game.is_player_human():
                    self.left_click(position)
                elif event.button == 3:
                    self.right_click(position)

            if event.type == KEYDOWN and event.key == K_ESCAPE and self.game.is_player_human():
                self.clear_move()
                self.view.draw_game(self.game)

            elif event.type == KEYDOWN and event.key == K_g:
                print self.game.gamestate

            elif self.quit_game_requested(event):
                self.exit_game()

            self.view.refresh()

    def exit_game(self):
        sys.exit()

    def get_input_upgrade(self, unit):
        self.view.draw_upgrade_options(unit)

        while True:
            event = pygame.event.wait()

            if event.type == KEYDOWN and event.key == K_1:
                return 0

            if event.type == KEYDOWN and event.key == K_2:
                return 1

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if within(event.pos, self.view.interface.upgrade_1_area):
                        return 0
                    elif within(event.pos, self.view.interface.upgrade_2_area):
                        return 1

            elif self.quit_game_requested(event):
                self.exit_game()

    def get_input_abilities(self, unit):
        self.view.draw_ask_about_ability(unit)

        while True:
            event = pygame.event.wait()

            if event.type == KEYDOWN and event.key == K_1:
                return 0

            if event.type == KEYDOWN and event.key == K_2:
                return 1

            elif self.quit_game_requested(event):
                self.exit_game()

    def ask_about_move_with_attack(self, action):

        self.view.draw_ask_about_move_with_attack(action.target_at)

        while True:
            event = pygame.event.wait()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = self.view.get_position_from_mouse_click(event.pos)

                if event.button == 1:
                    if position == action.target_at:
                        return True
                    if position == action.end_at:
                        return False

            elif self.quit_game_requested(event):
                self.exit_game()

    def pause(self):
        while True:
            event = pygame.event.wait()

            if self.quit_game_requested(event):
                self.exit_game()

            elif event.type == KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

    def upgrade_unit(self, position, unit):
        choice = self.get_input_upgrade(unit)

        if getattr(unit, "upgrades"):
            upgrade_choice = unit.upgrades[choice]
            upgraded_unit = Unit.make(unit.upgrades[choice])
        else:
            upgrade_choice = unit.get_upgrade_choice(choice)
            upgraded_unit = unit.get_upgraded_unit(upgrade_choice)

        upgrade_choice_to_save = upgrade_choice
        if not isinstance(upgrade_choice, basestring):
            upgrade_choice_to_save = readable(upgrade_choice)

        self.game.save_option("upgrade", upgrade_choice_to_save)
        if self.game.is_enemy_network():
            self.client.send_upgrade_choice(upgrade_choice_to_save, self.game.gamestate.action_count)

        self.game.gamestate.player_units[position] = upgraded_unit

    def perform_action(self, action, outcome=None, upgrade=None):
        self.view.draw_game(self.game)

        if self.game.is_player_human():

            if self.game.is_enemy_network():
                outcome = self.client.send_action(action.to_network(self.game.gamestate.action_count))
            else:
                outcome = Outcome.determine_outcome(action, self.game.gamestate)

            self.game.do_action(action, outcome)

            self.view.draw_game(self.game)
            self.view.draw_action(action, outcome, self.game)

            if action.move_with_attack is None:
                rolls = outcome.for_position(action.target_at)
                gamestate = self.game.gamestate
                push_possible = action.is_push() and action.attack_successful(rolls, gamestate)
                if push_possible or action.is_win(rolls, gamestate):
                    move_with_attack = self.ask_about_move_with_attack(action)
    
                    self.game.save_option("move_with_attack", move_with_attack)
                    if self.game.is_enemy_network():
                        self.client.send_move_with_attack(move_with_attack, gamestate.action_count)

                    if move_with_attack:
                        self.view.draw_post_movement(action)
                        gamestate.move_melee_unit_to_target_tile(outcome.for_position(action.target_at), action)

        else:
            if not outcome:
                outcome = Outcome.determine_outcome(action, self.game.gamestate)

            self.game.do_action(action, outcome)
            self.view.draw_action(action, outcome, self.game, flip=True)

        if action.is_attack():
            if settings.pause_for_attack_until_click:
                self.pause()
            else:
                pygame.time.delay(settings.pause_for_animation_attack)
        else:
            pygame.time.delay(settings.pause_for_animation)

        if self.game.gamestate.is_ended():
            self.game_end()
            return

        if self.game.is_player_human() and action.unit.is_milf():
            if action.is_attack() and action.target_at in self.game.gamestate.player_units:
                unit_position = action.target_at
            else:
                unit_position = action.end_at
            self.view.draw_game(self.game)
            self.upgrade_unit(unit_position, action.unit)
        elif self.game.is_player_network() and action.unit.is_milf():
            position = action.end_at
            if not position in self.game.gamestate.player_units:
                position = action.target_at
            upgraded_unit = action.unit.get_upgraded_unit(upgrade)
            self.game.gamestate.player_units[position] = upgraded_unit
            self.game.save_option("upgrade", upgrade)

        self.game.save(self.view, action, outcome)

        self.view.draw_game(self.game)

        if self.game.is_turn_done():
            self.game.shift_turn()

        self.view.draw_game(self.game)

        self.clear_move()

        if action.unit.has(State.extra_action) and self.game.is_player_human():
            position = action.end_at
            if not position in self.game.gamestate.player_units:
                position = action.target_at

            self.select_unit(position)

        print "Action performed. Expecting action from", self.game.current_player().intelligence

        if self.game.is_player_human():
            return
        elif self.game.is_player_network():
            print "Waiting for network action from network with number", self.game.gamestate.action_count + 1
            self.trigger_network_player()
        else:
            self.trigger_artificial_intelligence()

    def show_attack(self, attack_position):
        action = Action(self.game.gamestate.all_units(), self.start_at, target_at=attack_position)
        player_unit = self.game.gamestate.player_units[self.start_at]

        opponent_unit = self.game.gamestate.enemy_units[attack_position]
        self.view.show_attack(self.game.gamestate, action, player_unit, opponent_unit)

        return

    def show_unit(self, position):
        unit = None
        if position in self.game.gamestate.player_units:
            unit = self.game.gamestate.player_units[position]
        if position in self.game.gamestate.enemy_units:
            unit = self.game.gamestate.enemy_units[position]

        if unit:
            self.view.show_unit_zoomed(unit)
            self.pause()
            self.view.draw_game(self.game)
            return

    def quit_game_requested(self, event):
        return event.type == QUIT or (event.type == KEYDOWN and self.command_q_down(event.key))

    def command_q_down(self, key):
        return key == K_q and (pygame.key.get_mods() & KMOD_LMETA or pygame.key.get_mods() & KMOD_RMETA)

    def game_end(self):
        self.view.draw_game_end(self.game.current_player().color)
        self.pause()
        self.exit_game()

    def selecting_extra_action(self):
        return self.selected_unit and self.selected_unit.has(State.extra_action)

    def selecting_active_unit(self, position):
        if self.start_at and self.start_at == position:
            return False

        potential_actions = [action for action in self.game.gamestate.get_actions() if action.start_at == position]

        return position in self.game.gamestate.player_units and potential_actions

    def selecting_ability_target(self, position):
        if not self.start_at or position == self.start_at:
            return False

        return position in self.game.gamestate.all_units() and self.selected_unit.abilities

    def selecting_ranged_target(self, position):
        if not self.start_at:
            return False

        return position in self.game.gamestate.enemy_units and self.selected_unit.is_ranged()

    def selecting_melee_target(self, position):
        if not self.start_at:
            return False

        return position in self.game.gamestate.enemy_units and self.selected_unit.is_melee()

    def selecting_move(self, position):
        return self.start_at and position not in self.game.gamestate.all_units()


def within(point, area):
    return area[0].y <= point[1] <= area[1].y and area[0].x <= point[0] <= area[1].x
