package com.wotr.model.unit.special;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;
import com.wotr.model.unit.attribute.AttackAttribute;
import com.wotr.model.unit.attribute.DefenceAttribute;

public class Berserker extends MeleeUnit {

	public Berserker() {
		super("berserker", false);
	}

	@Override
	public AttackAttribute getAttack() {
		return new AttackAttribute(5);
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
		return 4;
	}

	@Override
	public UnitType getType() {
		return UnitType.INFANTRY;
	}
}
