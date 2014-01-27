package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.RangedUnit;

public class Ballista extends RangedUnit {

	public Ballista() {
		super("ballista", false);
	}

	@Override
	public int getAttack() {
		return 3;
	}

	@Override
	public int getDefence() {
		return 1;
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
