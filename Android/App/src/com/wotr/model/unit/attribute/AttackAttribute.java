package com.wotr.model.unit.attribute;

public class AttackAttribute extends Attribute {

	public AttackAttribute(int baseValue) {
		super(baseValue);
	}

	public int calculateValue() {
		return super.getValue() - getBonusValue();
	}

	public void addBonus(RawBonus bonus) {
		super.addBonus(bonus);
		listener.attackBonusChanged(getBonusValue());
	}	
}
