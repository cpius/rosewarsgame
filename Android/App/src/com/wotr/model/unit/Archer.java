package com.wotr.model.unit;

import com.wotr.GameManager;
import com.wotr.model.UnitType;
import com.wotr.strategy.battle.AttackStrategy;

public class Archer extends RangedUnit {

	public Archer() {
		super("archer", false);
	}

	@Override
	public int getAttack() {
		return 5;
	}

	@Override
	public int getDefense() {
		return 2;
	}

	@Override
	public int getMovement() {
		return 1;
	}

	@Override
	public int getRange() {
		return 4;
	}

	@Override
	public UnitType getType() {
		return UnitType.INFANTRY;
	}

	@Override
	public AttackStrategy getAttackStrategy() {
		return GameManager.getFactory().getArcherAttackStrategy();
	}
}
