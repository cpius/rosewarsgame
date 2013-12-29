package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.RangedUnit;

public class Catapult extends RangedUnit {

	public Catapult() {
		super("catapult", false);
	}

	@Override
	public int getAttack() {
		return 1;
	}

	@Override
	public int getDefence() {
		return 2;
	}

	@Override
	public int getMovement() {
		return 1;
	}

	@Override
	public int getRange() {
		return 3;
	}

	@Override
	public UnitType getType() {
		return UnitType.SIEGE_WEAPON;
	}

	public int getActionsUsedForAttack() {
		return 2;
	}

	public String getAttackSound() {
		return "sounds/catapult_attack.mp3";
	}
}
