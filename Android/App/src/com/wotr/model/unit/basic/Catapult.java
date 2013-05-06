package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.RangedUnit;
import com.wotr.model.unit.attribute.AttackAttribute;
import com.wotr.model.unit.attribute.DefenceAttribute;

public class Catapult extends RangedUnit {

	public Catapult() {
		super("catapult", false);
	}

	@Override
	public AttackAttribute getAttack() {
		return new AttackAttribute(1);
	}

	@Override
	public DefenceAttribute getDefense() {
		return new DefenceAttribute(2);
	}

	@Override
	public int getMovement() {
		return 1;
	}

	@Override
	public int getRange() {
		return 3;
	}

	@Override
	public UnitType getType() {
		return UnitType.SIEGE_WEAPON;
	}

	public int getActionsUsedForAttack() {
		return 2;
	}

	public String getAttackSound() {
		return "sounds/catapult_attack.wav";
	}
}
