package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;

public class LightCavalry extends MeleeUnit {

	public LightCavalry() {
		super("lightcavalry", false);
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
		return 4;
	}

	@Override
	public int getRange() {
		return 1;
	}
	
	@Override
	public UnitType getType() {
		return UnitType.CAVALRY;
	}
	
	public String getAttackSound() {
		return "sounds/swords.mp3";
	}
}
