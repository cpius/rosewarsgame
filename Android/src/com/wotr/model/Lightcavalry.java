package com.wotr.model;

public class LightCavalry extends AbstractCard {

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
}
