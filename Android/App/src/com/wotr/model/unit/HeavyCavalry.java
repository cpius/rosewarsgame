package com.wotr.model.unit;

public class HeavyCavalry extends MeleeUnit {

	public HeavyCavalry() {
		super("heavycavalry", false);
	}

	@Override
	public int getAttack() {
		return 3;
	}

	@Override
	public int getDefense() {
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
}
