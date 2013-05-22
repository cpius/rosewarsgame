package com.wotr.model.attack;

import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public abstract class AbstractAttackEndPosition implements AttackEndPosition {

	private Position position;
	protected final Unit attackingUnit;
	private AttackResult attackResult;

	public AbstractAttackEndPosition(Unit attackingUnit, Position position) {
		this.attackingUnit = attackingUnit;
		this.position = position;
	}

	@Override
	public Position getPosition() {
		return position;
	}

	public abstract void endAttack();

	@Override
	public void setAttackResult(AttackResult attackResult) {
		this.attackResult = attackResult;
	}

	@Override
	public AttackResult getAttackResult() {
		return attackResult;
	}
}
