package com.wotr.model.unit.special;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;

public class Berserker extends MeleeUnit {

	public Berserker() {
		super("berserker", false);
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
}
