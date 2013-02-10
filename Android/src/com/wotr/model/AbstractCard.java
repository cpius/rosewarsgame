package com.wotr.model;


public abstract class AbstractCard {

	private final String image;

	private Position posistion;

	public String getImage() {
		return image;
	}

	public AbstractCard(String image) {
		this.image = image;
	}

	public Position getPosistion() {
		return posistion;
	}

	public void setPosistion(Position posistion) {
		this.posistion = posistion;
	}
}
