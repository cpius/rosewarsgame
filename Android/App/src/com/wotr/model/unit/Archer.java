package com.wotr.model.unit;

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
}
