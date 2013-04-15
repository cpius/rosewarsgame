package com.wotr.model.unit;

import com.wotr.GameManager;
import com.wotr.model.Position;
import com.wotr.model.UnitType;
import com.wotr.strategy.action.UnitActionResolverStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.BonusStrategy;
import com.wotr.strategy.battle.DefenceStrategy;

public abstract class Unit implements Cloneable {

	private final String image;
	private Position position;
	private boolean enemy;

	private int experiencePoints = 0;
	private int attackBonus = 0;
	private int defenceBonus = 0;

	public String getImage() {
		return "unit/" + image + (enemy ? "red" : "green") + ".jpg";
	}

	public Unit(String image, boolean enemy) {
		this.image = image;
		this.enemy = enemy;
	}

	protected abstract int getAttack();

	protected abstract int getDefense();

	public abstract int getMovement();

	public abstract int getRange();

	public abstract UnitActionResolverStrategy getActionResolverStrategy();

	public abstract boolean isRanged();

	public abstract UnitType getType();

	public Position getPosition() {
		return position;
	}

	public void setPosition(Position position) {
		this.position = position;
	}
	
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
	
	public BonusStrategy getBonusStrategy() {
		return GameManager.getFactory().getBonusStrategy();
	}

	public int getActionsUsedForAttack() {
		return 1;
	}

	public String getKilledSound() {
		return "sounds/pain.mp3";
	}

	public String getAttackSound() {
		return "sounds/sword_sound.wav";
	}

	public String getDefenceSound() {
		return null;
	}

	public int getAttackWithUnitBonus() {
		return getAttack() - getAttackBonus();
	}

	public int getDefenseWithUnitBonus() {
		return getDefense() + getDefenceBonus();
	}

	public void addAttackBonus() {
		attackBonus++;
		experiencePoints = 0;
	}

	public void addDefenceBonus() {
		defenceBonus++;
		experiencePoints = 0;
	}

	public int getExperiencePoints() {
		return experiencePoints;
	}

	public int getAttackBonus() {
		return attackBonus;
	}

	public int getDefenceBonus() {
		return defenceBonus;
	}
}
