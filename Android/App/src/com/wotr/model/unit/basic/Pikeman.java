package com.wotr.model.unit.basic;

import com.wotr.GameManager;
import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;
import com.wotr.strategy.battle.AttackStrategy;

public class Pikeman extends MeleeUnit {

	public Pikeman() {
		super("pikeman", false);
	}

	@Override
	protected int getAttack() {
		return 5;
	}

	@Override
	protected int getDefense() {
		return 2;
	}

	@Override
	public int getMovement() {
		return 1;
	}

	@Override
	public int getRange() {
		return 1;
	}

	@Override
	public UnitType getType() {
		return UnitType.INFANTRY;
	}

	public UnitType[] getZoc() {
		UnitType[] zoc = { UnitType.CAVALRY };
		return zoc;
	}
	
	@Override
	public AttackStrategy getAttackStrategy() {
		return GameManager.getFactory().getPikemanAttackStrategy();
	}
}
