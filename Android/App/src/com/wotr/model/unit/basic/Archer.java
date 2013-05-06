package com.wotr.model.unit.basic;

import com.wotr.GameManager;
import com.wotr.model.UnitType;
import com.wotr.model.unit.RangedUnit;
import com.wotr.model.unit.attribute.AttackAttribute;
import com.wotr.model.unit.attribute.DefenceAttribute;
import com.wotr.strategy.battle.AttackStrategy;

public class Archer extends RangedUnit {

	public Archer() {
		super("archer", false);
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

	@Override
	public AttackStrategy getAttackStrategy() {
		return GameManager.getFactory().getArcherAttackStrategy();
	}
}
