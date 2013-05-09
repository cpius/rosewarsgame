package com.wotr.model.unit.attribute;

public class DefenceAttribute extends Attribute {

	public DefenceAttribute(int baseValue) {
		super(baseValue);
	}

	public int calculateValue() {
		return getValue();
	}

	public void addBonus(RawBonus bonus) {
		super.addBonus(bonus);
		listener.defenceBonusChanged(getBonusValue());
	}
}
