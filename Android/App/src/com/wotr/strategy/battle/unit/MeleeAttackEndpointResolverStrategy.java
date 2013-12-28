package com.wotr.strategy.battle.unit;

import java.util.ArrayList;
import java.util.Collection;

import com.wotr.model.ActionPath;
import com.wotr.model.Position;
import com.wotr.model.attack.AttackEndPosition;
import com.wotr.model.attack.FailedMeleeAttackEndpoint;
import com.wotr.model.attack.SuccessfulMeleeAttackEndpoint;
import com.wotr.model.unit.MeleeUnit;
import com.wotr.strategy.battle.AttackEndpointResolverStrategy;
import com.wotr.strategy.game.AttackEnder;

public class MeleeAttackEndpointResolverStrategy implements AttackEndpointResolverStrategy {

	protected MeleeUnit meleeUnit;

	public MeleeAttackEndpointResolverStrategy(MeleeUnit meleeUnit) {
		this.meleeUnit = meleeUnit;
	}

	@Override
	public Collection<AttackEndPosition> getAttackEndpointPositions(AttackEnder ender, boolean success, ActionPath actionPath) {
		Collection<AttackEndPosition> result = new ArrayList<AttackEndPosition>();

		if (success) {

			// Add the last point of path
			Position position = getPathEnd(meleeUnit, actionPath);
			result.add(new SuccessfulMeleeAttackEndpoint(ender, meleeUnit, position));

			// Add the position of the defeated unit
			result.add(new SuccessfulMeleeAttackEndpoint(ender, meleeUnit, actionPath.getPosition()));

		} else {

			Position position = getPathEnd(meleeUnit, actionPath);
			result.add(new FailedMeleeAttackEndpoint(ender, meleeUnit, position));
		}
		return result;
	}

	protected Position getPathEnd(MeleeUnit meleeUnit, ActionPath actionPath) {
		if (actionPath.getPreviousPath() != null) {
			return actionPath.getPreviousPath().getPosition();
		} else {
			return meleeUnit.getPosition();
		}
	}
}
