package com.wotr.strategy.battle.unit;

import java.util.ArrayList;
import java.util.Collection;

import com.wotr.model.ActionPath;
import com.wotr.model.attack.AttackEndPosition;
import com.wotr.model.attack.FailedRangedAttackEndpoint;
import com.wotr.model.attack.SuccessfulRangedAttackEndpoint;
import com.wotr.model.unit.RangedUnit;
import com.wotr.strategy.battle.AttackEndpointResolverStrategy;
import com.wotr.strategy.game.AttackEnder;

public class RangedAttackEndpointResolverStrategy implements AttackEndpointResolverStrategy {

	private RangedUnit rangedUnit;

	public RangedAttackEndpointResolverStrategy(RangedUnit rangedUnit) {
		this.rangedUnit = rangedUnit;
	}

	@Override
	public Collection<AttackEndPosition> getAttackEndpointPositions(AttackEnder ender, boolean success, ActionPath actionPath) {
		Collection<AttackEndPosition> result = new ArrayList<AttackEndPosition>();

		if (success) {
			result.add(new SuccessfulRangedAttackEndpoint(ender, rangedUnit, rangedUnit.getPosition()));
		} else {
			result.add(new FailedRangedAttackEndpoint(ender, rangedUnit, rangedUnit.getPosition()));
		}
		return result;
	}
}
