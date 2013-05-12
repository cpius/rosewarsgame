package com.wotr.model.unit;

import com.wotr.GameManager;
import com.wotr.model.Position;
import com.wotr.model.UnitType;
import com.wotr.model.unit.attribute.AttackAttribute;
import com.wotr.model.unit.attribute.DefenceAttribute;
import com.wotr.strategy.action.UnitActionResolverStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.DefenceStrategy;

public abstract class Unit implements Cloneable {

	private final String image;
	private Position position;
	private boolean enemy;

	private int experiencePoints = 0;

	private AttackAttribute attackAttribute;
	private DefenceAttribute defenceAttribute;
	
	public String getImage() {
		return "unit/" + image + (enemy ? "red" : "green") + ".jpg";
	}

	public Unit(String image, boolean enemy) {
		this.image = image;
		this.enemy = enemy;
	}

	public abstract int getDefence();

	public abstract int getAttack();

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

	public int getExperiencePoints() {
		return experiencePoints;
	}

	public AttackAttribute getAttackAttribute() {
		if (attackAttribute == null) {
			attackAttribute = new AttackAttribute(getAttack());
		}
		return attackAttribute;
	}

	public DefenceAttribute getDefenceAttribute() {
		if (defenceAttribute == null) {
			defenceAttribute = new DefenceAttribute(getDefence());
		}
		return defenceAttribute;
	}

	public void addExperience() {
		experiencePoints++;
	}
	
	public void resetExperience() {
		experiencePoints = 0;
	}
}
