package com.wotr.model.unit.attribute;

import java.io.Serializable;

public class AttackAttribute extends Attribute implements Serializable {

	public AttackAttribute(int baseValue) {
		super(baseValue);
	}

	public int calculateValue() {
		return super.getValue() - getBonusValue();
	}

	public void addBonus(RawBonus bonus) {
		super.addBonus(bonus);
		if (listener != null)
			listener.attackBonusChanged(getBonusValue());
	}
}
