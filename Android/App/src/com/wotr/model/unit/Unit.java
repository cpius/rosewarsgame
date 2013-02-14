package com.wotr.model.unit;

import com.wotr.model.Position;
import com.wotr.strategy.action.ActionResolverStrategy;

public abstract class Unit {

	private final String image;
	private Position posistion;
	private final boolean enemy;

	public String getImage() {
		return image + (enemy ? "red" : "green") + ".jpg";
	}

	public Unit(String image, boolean enemy) {
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

	public abstract ActionResolverStrategy getActionResolverStrategy();

	public abstract boolean isRanged();
}
