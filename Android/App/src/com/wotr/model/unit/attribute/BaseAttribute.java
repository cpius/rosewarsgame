package com.wotr.model.unit.attribute;

import java.io.Serializable;

public abstract class BaseAttribute implements Serializable {

	private final int baseValue;
	private Attribute parent;

	public BaseAttribute(int baseValue) {
		this.baseValue = baseValue;
	}

	public int getValue() {
		return baseValue;
	}

	public void setParent(Attribute parent) {
		this.parent = parent;
	}

	public Attribute getParent() {
		return parent;
	}
}
