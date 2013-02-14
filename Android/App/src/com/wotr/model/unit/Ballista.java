package com.wotr.model.unit;

public class Ballista extends RangedUnit {

	public Ballista() {
		super("ballista", false);
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
