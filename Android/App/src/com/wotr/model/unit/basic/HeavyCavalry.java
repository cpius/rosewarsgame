package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;
import com.wotr.model.unit.attribute.AttackAttribute;
import com.wotr.model.unit.attribute.DefenceAttribute;

public class HeavyCavalry extends MeleeUnit {

	public HeavyCavalry() {
		super("heavycavalry", false);
	}

	@Override
	public AttackAttribute getAttack() {
		return new AttackAttribute(4);
	}

	@Override
	public DefenceAttribute getDefense() {
		return new DefenceAttribute(3);
	}

	@Override
	public int getMovement() {
		return 2;
	}

	@Override
	public int getRange() {
		return 1;
	}
	
	@Override
	public UnitType getType() {
		return UnitType.CAVALRY;
	}
	
	public String getAttackSound() {
		return "sounds/swords.mp3";
	}
}
