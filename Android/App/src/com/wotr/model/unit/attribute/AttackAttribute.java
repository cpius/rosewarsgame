package com.wotr.model.unit.attribute;

public class AttackAttribute extends Attribute {

	public AttackAttribute(int baseValue) {
		super(baseValue);
	}

	public int calculateValue() {
		return getValue();
	}

	public void addBonus(RawBonus bonus) {
		super.addBonus(bonus);
		listener.attackBonusChanged(getBonusValue());
	}
}
