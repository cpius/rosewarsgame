package com.wotr.model.attack;

import com.wotr.model.Position;
import com.wotr.model.unit.RangedUnit;
import com.wotr.strategy.game.AttackEnder;

public class FailedRangedAttackEndpoint extends AbstractAttackEndPosition implements AttackEndPosition {

	private final AttackEnder ender;

	public FailedRangedAttackEndpoint(AttackEnder ender, RangedUnit attackingUnit, Position position) {
		super(attackingUnit, position);
		this.ender = ender;
	}

	@Override
	public void endAttack() {
		ender.endAttack(attackingUnit, getPosition(), false);
	}
}
