package com.wotr.model;

public abstract class AbstractCard {

	private final String image;
	private Position posistion;
	private final boolean enemy;

	public String getImage() {
		return image + (enemy ? "red" : "green") + ".jpg";
	}

	public AbstractCard(String image, boolean enemy) {
		this.image = image;
		this.enemy = enemy;
	}

	public Position getPosistion() {
		return posistion;
	}

	public void setPosistion(Position posistion) {
		this.posistion = posistion;
	}

	public abstract int getAttack();

	public abstract int getDefense();

	public abstract int getMovement();

	public abstract int getRange();
}
