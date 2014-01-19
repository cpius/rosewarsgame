package com.wotr.model.attack;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.AttackEnder;

public class FailedMeleeAttackEndpoint extends AbstractAttackEndPosition implements AttackEndPosition {

	private final AttackEnder ender;

	public FailedMeleeAttackEndpoint(AttackEnder ender, Unit attackingUnit, Position position) {
		super(attackingUnit, position);
		this.ender = ender;
	}

	@Override
	public void endAttack() {
		ender.endAttack(attackingUnit, getPosition(), !attackingUnit.getPosition().equals(getPosition()));
	}
	
}
