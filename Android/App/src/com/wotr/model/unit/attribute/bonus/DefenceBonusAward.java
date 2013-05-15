package com.wotr.model.unit.attribute.bonus;

import com.wotr.model.unit.Unit;
import com.wotr.model.unit.attribute.RawBonus;

public class DefenceBonusAward implements BonusAward {

	private final Unit unit;

	public DefenceBonusAward(Unit unit) {
		this.unit = unit;
	}

	@Override
	public void claim() {
		unit.getDefenceAttribute().addBonus(new RawBonus(1));
	}
}
