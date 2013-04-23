package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;

public class HeavyCavalry extends MeleeUnit {

	public HeavyCavalry() {
		super("heavycavalry", false);
	}

	@Override
	protected int getAttack() {
		return 4;
	}

	@Override
	protected int getDefense() {
		return 3;
	}

	@Override
	public int getMovement() {
		return 2;
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
