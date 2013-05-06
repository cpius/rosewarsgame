package com.wotr.model.unit.attribute;

public class DefenceAttribute extends BaseAttribute {

	private final int baseValue;

	public DefenceAttribute(int baseValue) {
		this.baseValue = baseValue;
	}

	public int calculateValue() {
		return baseValue;
	}
}
