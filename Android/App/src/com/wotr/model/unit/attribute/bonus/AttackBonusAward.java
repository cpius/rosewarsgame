package com.wotr.model.unit.attribute.bonus;

import com.wotr.model.unit.Unit;
import com.wotr.model.unit.attribute.RawBonus;

public class AttackBonusAward implements BonusAward {

	private final Unit unit;

	public AttackBonusAward(Unit unit) {
		this.unit = unit;
	}

	@Override
	public void claim() {
		unit.getAttackAttribute().addBonus(new RawBonus(1));
	}
}
