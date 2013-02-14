package com.wotr.model.unit;

import com.wotr.strategy.action.ActionResolverStrategy;
import com.wotr.strategy.facade.ActionResolverFactory;

public abstract class MeleeUnit extends Unit {

	public MeleeUnit(String image, boolean enemy) {
		super(image, enemy);
	}

	public boolean isRanged() {
		return false;
	}
	
	@Override
	public ActionResolverStrategy getActionResolverStrategy() {
		return ActionResolverFactory.getMeleeActionResolverStrategy();
	}
}
