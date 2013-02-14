package com.wotr.model.unit;

import com.wotr.strategy.action.ActionResolverStrategy;
import com.wotr.strategy.facade.ActionResolverFactory;

public abstract class RangedUnit extends Unit {

	public RangedUnit(String image, boolean enemy) {
		super(image, enemy);
	}

	public boolean isRanged() {
		return true;
	}

	@Override
	public ActionResolverStrategy getActionResolverStrategy() {
		return ActionResolverFactory.getRangedActionResolverStrategy();
	}
}
