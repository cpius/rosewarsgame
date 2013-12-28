package com.wotr.strategy.battle.unit;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import com.wotr.model.Action;
import com.wotr.model.ActionPath;
import com.wotr.model.Position;
import com.wotr.model.attack.AttackEndPosition;
import com.wotr.model.attack.FailedMeleeAttackEndpoint;
import com.wotr.model.attack.SuccessfulMeleeAttackEndpoint;
import com.wotr.model.unit.special.Chariot;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.battle.AttackEndpointResolverStrategy;
import com.wotr.strategy.game.AttackEnder;
import com.wotr.strategy.game.Game;

public class ChariotAttackEndpointResolverStrategy extends MeleeAttackEndpointResolverStrategy implements AttackEndpointResolverStrategy {

	private Game game;

	public ChariotAttackEndpointResolverStrategy(Chariot chariot, Game game) {
		super(chariot);
		this.game = game;
	}

	@Override
	public Collection<AttackEndPosition> getAttackEndpointPositions(AttackEnder ender, boolean success, ActionPath actionPath) {
		Set<AttackEndPosition> result = new HashSet<AttackEndPosition>();

		// Add attacking and next to attacking position as endpoint
		result.addAll(super.getAttackEndpointPositions(ender, success, actionPath));

		ActionsResolverStrategy actionsResolver = game.getActionsResolver();

		Position position = getPathEnd(meleeUnit, actionPath);
		Collection<Action> remainingMoveActions = actionsResolver.getRemainingMoveActions(meleeUnit, position, actionPath.getPathLength() + 1);

		if (success) {
			remainingMoveActions.addAll(actionsResolver.getRemainingMoveActions(meleeUnit, actionPath.getPosition(), actionPath.getPathLength() + 1));
		}

		result.addAll(getAttackEndPositions(ender, remainingMoveActions, success));
		return result;
	}

	private Collection<? extends AttackEndPosition> getAttackEndPositions(AttackEnder ender, Collection<Action> remainingMoveActions, boolean success) {
		Set<AttackEndPosition> result = new HashSet<AttackEndPosition>();
		for (Action action : remainingMoveActions) {
			if (success) {
				result.add(new SuccessfulMeleeAttackEndpoint(ender, meleeUnit, action.getPosition()));
			} else {
				result.add(new FailedMeleeAttackEndpoint(ender, meleeUnit, action.getPosition()));
			}
		}
		return result;
	}
}
