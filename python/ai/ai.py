from gamestate.gamestate_library import *
from gamestate import battle
from gamestate.gamestate_module import Gamestate
from functools import partial
from ai import ai_factors
from operator import attrgetter
from ai.ai_library import Result, success, failure, Player
import gamestate.action_getter as action_getter
import ai.documenter as documenter


class AI():
    def __init__(self):
        self.select_action = select_action
        self.select_upgrade = select_upgrade


def document_actions(actions, path):
    documenter.document_actions(actions, path)


def select_upgrade(gamestate):
    return 1


def select_action(gamestate):
    scorer = ai_factors.FactorScorer()
    actions = score_actions(gamestate, set(), scorer)
    win_actions = {action for action in actions if Result.noresult in action.factors and
                   "Backline" in action.factors[Result.noresult][Player.player]}
    if win_actions:
        for action in win_actions:
            action.move_distance = distance(action.start_at, action.end_at)
        chosen_action = min(win_actions, key=attrgetter("move_distance"))
    else:
        chosen_action = max(actions, key=attrgetter("total_score"))

    update_references(chosen_action, gamestate)
    return chosen_action


def chance_of_win(gamestate, action):
    """
    :param gamestate: A gamestate
    :param action: An attack
    :return: The chance that the attack is successful
    """
    attack = battle.get_attack(action, gamestate)
    defence = battle.get_defence(action, attack, gamestate)
    attack = min(max(0, attack), 6)
    defence = min(max(0, defence), 6)

    chance_of_attack_successful = attack / 6
    chance_of_defence_unsuccessful = (6 - defence) / 6

    return chance_of_attack_successful * chance_of_defence_unsuccessful


def update_references(action, gamestate):
    """
    :param action: An action
    :param gamestate: A gamestate
    :return: An action in which .unit and .target_unit refers to objects in the supplied gamestate.
    """
    units = merge(gamestate.player_units, gamestate.enemy_units)
    action.unit = units[action.start_at]
    if action.target_at and action.target_at in units:
        action.target_unit = units[action.target_at]
    return action


def one_action_forward(gamestate_document, action, outcome=None):
    """
    :param gamestate_document: A dictionary containing the gamestate
    :param action: An action
    :param outcome: An outcome of the action if applicable
    :return: The resulting gamestate after performing action. (Including new bonus tiles.)
    """
    gamestate = Gamestate.from_document(gamestate_document)
    action = update_references(action, gamestate)
    gamestate.bonus_tiles = action_getter.get_bonus_tiles(gamestate)
    gamestate.do_action(action, outcome)
    return gamestate


def score_actions(gamestate, scored_actions, scorer):
    """
    :param gamestate: A gamestate
    :param scored_actions: A set of actions whose scores are already evaluated.
    :return: A list of actions with attributes score and total_score.
             "score" is the value of the action itself.
             "total_score" is the value of the action plus the best subsequent action if applicable.
    """

    def find_score(result):
        """
        :param result: The result of an action. If the action has an outcome the result can be either win or loss. If
                       the action does not have an outcome, the result is noresult.

        Adds the factors for the resulting gamestate to the factors dictionary of the action, and adds the score of the
        resulting gamestate to the score_if dictionary of the action.
        """
        gamestate_factors = ai_factors.get_factors(gamestate_2[action][result])
        action.factors[result] = ai_factors.get_differences(gamestate_factors, original_factors)
        action.score_if[result] = scorer.get_score(action.factors[result])

    # Make a copy of the gamestate
    gamestate_1_document = gamestate.to_document()
    gamestate_1 = Gamestate.from_document(gamestate_1_document)

    # Find the available actions.
    gamestate_1.set_available_actions()
    all_actions = gamestate_1.get_actions()

    # Only calculate scores for actions that are not already scored.
    new_actions = {action for action in all_actions if action not in scored_actions}
    actions_new_bonus = {action for action in all_actions if action.end_at in gamestate.bonus_tiles[Trait.flag_bearing]
                         or action.start_at in gamestate.bonus_tiles[Trait.crusading]}
    actions = new_actions | actions_new_bonus
    scoredict = {action: action.score for action in scored_actions}
    for action in all_actions:
        if action in scoredict:
            action.score = scoredict[action]

    # If there are no actions whose scores are not already calculated, skip the remaining steps.
    if not actions:
        return all_actions

    # Contains the new gamestates after each action and each result.
    gamestate_2 = {}

    # The factors of gamestate_1. A factor is an element of the gamestate that is important.
    original_factors = ai_factors.get_factors(gamestate_1)

    # Define a function that returns the resulting gamestate after performing an action on gamestate_1.
    # (Without changing gamestate_1.)
    perform_action = partial(one_action_forward, gamestate_1_document)

    # For each action, calculate the score of the action itself.
    for action in actions:
        action.factors, action.score_if = {}, {}  # Contains the factors and scores after each possible result.
        gamestate_2[action] = {}  # Contains the gamestate after each possible results.

        if action.has_outcome:
            gamestate_2[action][Result.win] = perform_action(action, success)
            gamestate_2[action][Result.loss] = perform_action(action, failure)
            action.chance_of_win = chance_of_win(gamestate_1, action)
            find_score(Result.win)
            find_score(Result.loss)
            action.score = (action.score_if[Result.win] * action.chance_of_win +
                            action.score_if[Result.loss] * (1 - action.chance_of_win))

        else:
            gamestate_2[action][Result.noresult] = perform_action(action)
            find_score(Result.noresult)
            action.score = action.score_if[Result.noresult]

    # For each action (and each result), find the best next action and its score.
    for action in actions:
        if next(iter(gamestate_2[action].values())).actions_remaining:
            action.next_action = {}  # Contains the best next action after each possible result.
            if action.has_outcome:
                next_actions_if_win = score_actions(gamestate_2[action][Result.win], actions, scorer)
                action.next_action[Result.win] = max(next_actions_if_win, key=attrgetter("score"))

                next_actions_if_loss = score_actions(gamestate_2[action][Result.loss], actions, scorer)
                action.next_action[Result.loss] = max(next_actions_if_loss, key=attrgetter("score"))

            else:
                next_actions = score_actions(gamestate_2[action][Result.noresult], actions, scorer)
                action.next_action[Result.noresult] = max(next_actions, key=attrgetter("score"))

    # For each action, calculate the total score. The total score is the value of the action and the expected value
    # of the best next action if applicable.
    for action in actions:
        if hasattr(action, "next_action"):
            if action.has_outcome:
                action.total_score = (action.score + action.next_action[Result.win].score * action.chance_of_win +
                                      action.next_action[Result.loss].score * (1 - action.chance_of_win))
            else:
                action.total_score = action.score + action.next_action[Result.noresult].score
        else:
            action.total_score = action.score

    return all_actions
