package com.wotr.model.unit.attribute;

import java.util.ArrayList;
import java.util.Collection;

public abstract class Attribute extends BaseAttribute {

	Collection<RawBonus> bonusCollection = new ArrayList<RawBonus>();
	protected BonusListener listener;

	public Attribute(int baseValue) {
		super(baseValue);
	}

	public void addBonus(RawBonus bonus) {
		bonusCollection.add(bonus);
		bonus.setParent(this);
	}

	public int getBonusValue() {
		int bonus = 0;
		for (RawBonus rawBonus : bonusCollection) {
			bonus += rawBonus.getValue();
		}
		return bonus;
	}

	public void addBonusListener(BonusListener listener) {
		this.listener = listener;
	}

}
