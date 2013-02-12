package com.wotr.model;

public class Pikeman extends AbstractCard {

	public Pikeman() {
		super("pikeman", false);
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
		return 1;
	}
}
