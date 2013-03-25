package com.wotr.model.unit;

import com.wotr.GameManager;
import com.wotr.model.Position;
import com.wotr.model.UnitType;
import com.wotr.strategy.action.ActionResolverStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.DefenceStrategy;

public abstract class Unit implements Cloneable {

	private final String image;
	private Position posistion;
	private boolean enemy;

	public String getImage() {
		return "unit/" + image + (enemy ? "red" : "green") + ".jpg";
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

	public abstract UnitType getType();
	
	public UnitType[] getZoc() {
		return new UnitType[0];
	}

	@Override
	protected Object clone() throws CloneNotSupportedException {
		return super.clone();
	}

	public boolean isEnemy() {
		return enemy;
	}

	public void setEnemy(boolean enemy) {
		this.enemy = enemy;
	}

	public AttackStrategy getAttackStrategy() {
		return GameManager.getFactory().getAttackStrategy();
	}

	public DefenceStrategy getDefenceStrategy() {
		return GameManager.getFactory().getDefenceStrategy();
	}
	
	public int getActionsUsedForAttack() {
		return 1;
	}
}
