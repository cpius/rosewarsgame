from gamestate.gamestate_library import *
from gamestate.action import Action
import gamestate.battle as battle


def settle_attack(action, gamestate, outcome, attack_direction, is_sub_action=False):
    """
    :param action: The action or sub_action being performed
    :param gamestate: The Gamestate
    :param outcome: The Outcome
    :param attack_direction: The direction from end_at to target_at of the main action
    :param is_sub_action: Whether or not the action is a sub_action.
    (Doesn't make any difference with current rules.)
    :return: None
    """
    all_units = gamestate.all_units()
    rolls = outcome.for_position(action.target_at)

    if battle.is_win(action, rolls, gamestate, is_sub_action):
        if action.target_unit.has_extra_life:
            action.target_unit.set(State.lost_extra_life)
        else:
            gamestate.delete_unit_at(action.target_at)

    elif action.is_push and battle.attack_successful(action, rolls, gamestate):  # Unit is pushed
        push_destination = action.target_at.move(attack_direction)

        if push_destination in all_units or not push_destination:
            if action.target_unit.has_extra_life:
                action.target_unit.set(State.lost_extra_life)
            else:
                gamestate.delete_unit_at(action.target_at)
        else:
            gamestate.move_unit(action.target_at, push_destination)

    if battle.flanking(action):
        action.target_unit.set(State.flanked)

    if action.is_javelin_throw:
        action.unit.set(State.javelin_thrown)


def do_action(gamestate, action, outcome):

    def settle_ability():
        ability = action.ability
        level = unit.get_level(action.ability)

        if ability == Ability.bribe:
            target_unit.set(Effect.bribed, duration=1)
            gamestate.change_unit_owner(target_at)

        elif ability == Ability.assassinate:
            rolls = outcome.for_position(action.target_at)
            if battle.assassin_kills_target(rolls, level):
                gamestate.delete_unit_at(target_at)

            rolls = outcome.for_position(action.start_at)
            if battle.assassin_dies(rolls):
                gamestate.delete_unit_at(start_at)

        elif ability == Ability.poison:
            target_unit.set(Effect.poisoned, level=level, duration=level)

        elif ability == Ability.sabotage:
            target_unit.set(Effect.sabotaged, level=level, duration=level)

        elif ability == Ability.improve_weapons:
            target_unit.set(Effect.improved_weapons, level=level, duration=level)

    def prepare_extra_actions():
        # If this is the extra action already, remove the option to do more extra actions
        if unit.has(State.extra_action):
            unit.remove(State.extra_action)
            unit.remove(State.movement_remaining)
            return

        # If the action is a move with a Hobelar, there is no reason to allow an extra action.
        if unit.has(Trait.swiftness) and not action.is_attack:
            return

        if movement_remaining or unit.has(Trait.combat_agility):
            unit.set(State.extra_action)

    def update_actions_remaining():

        if unit.has(State.extra_action):
            return

        gamestate.decrement_actions_remaining()

        if action.double_cost:
            gamestate.decrement_actions_remaining()

    def apply_unit_effects():
        if unit.has(Trait.attack_cooldown) and action.is_attack:
            unit.set(State.attack_frozen, value=3)

        if unit.has(Trait.attack_cooldown, 2) and action.is_attack:
            unit.set(State.attack_frozen, value=2)

    def unit_should_gain_experience():
        return action.is_attack or unit.type == Type.Cavalry or action.is_ability

    def get_subattack_targets():
        targets = []
        if unit.has(Trait.triple_attack):
            targets = action.end_at.two_forward_tiles(attack_direction) & set(enemy_units)
        elif unit.has(Trait.spread_attack):
            targets = list(action.target_at.adjacent_tiles() & set(all_units))
        elif unit.has(Trait.longsword):
            targets = list(action.end_at.four_forward_tiles(attack_direction) & set(enemy_units))

        return targets

    def unit_has_subattacks():
        subattack_traits = [Trait.triple_attack, Trait.spread_attack, Trait.longsword]

        return any(unit.has(trait) for trait in subattack_traits)

    def unit_has_extra_action_trait():
        return any(unit.has(attribute) for attribute in [Trait.swiftness, Trait.combat_agility])

    # Define local variables
    start_at = action.start_at
    end_at = action.end_at
    target_at = action.target_at
    unit = action.unit
    target_unit = action.target_unit
    enemy_units = gamestate.enemy_units
    all_units = gamestate.all_units()

    apply_unit_effects()

    update_actions_remaining()

    gamestate.move_unit(start_at, end_at)
    final_position = end_at

    if unit_should_gain_experience():
        unit.gain_experience()

    if action.is_attack:
        attack_direction = action.attack_direction
        settle_attack(action, gamestate, outcome, attack_direction, False)

        if action.move_with_attack and action.target_at not in enemy_units:
            gamestate.move_unit(end_at, target_at)
            final_position = target_at

        if unit_has_subattacks():
            for target in get_subattack_targets():
                sub_attack = Action(all_units, start_at, end_at, target)
                settle_attack(sub_attack, gamestate, outcome, attack_direction, True)

    elif action.is_ability:
        settle_ability()

    # Determine the movement points the unit can use on its extra action.
    movement_remaining = unit.movement - distance(start_at, final_position)

    # An attack requires a movement point even if it doesn't succeed. But not for Fencer.
    if action.is_attack and not unit.has(Trait.combat_agility) and target_at != final_position:
        movement_remaining -= 1

    unit.set(State.movement_remaining, value=movement_remaining)

    if unit_has_extra_action_trait():
        prepare_extra_actions()

    unit.set(State.used, value=1)
