package com.wotr.model;

public class Catapult extends AbstractCard {
	
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
}
