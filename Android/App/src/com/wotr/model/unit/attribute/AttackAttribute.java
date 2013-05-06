package com.wotr.model.unit.attribute;

public class AttackAttribute extends BaseAttribute {

	private final int baseValue;

	public AttackAttribute(int baseValue) {
		this.baseValue = baseValue;
	}

	public int calculateValue() {
		return baseValue;
	}
}
