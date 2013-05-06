package com.wotr.model.unit.basic;

import com.wotr.model.UnitType;
import com.wotr.model.unit.RangedUnit;
import com.wotr.model.unit.attribute.AttackAttribute;
import com.wotr.model.unit.attribute.DefenceAttribute;

public class Ballista extends RangedUnit {

	public Ballista() {
		super("ballista", false);
	}

	@Override
	public AttackAttribute getAttack() {
		return new AttackAttribute(3);
	}

	@Override
	public DefenceAttribute getDefense() {
		return new DefenceAttribute(1);
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
}
