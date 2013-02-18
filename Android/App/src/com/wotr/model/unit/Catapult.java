package com.wotr.model.unit;

import com.wotr.model.UnitType;

public class Catapult extends RangedUnit {

	public Catapult() {
		super("catapult", false);
	}

	@Override
	public int getAttack() {
		return 1;
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
		return 3;
	}

	@Override
	public UnitType getType() {
		return UnitType.SIEGE_WEAPON;
	}
}
