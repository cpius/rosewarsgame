package com.wotr.strategy.facade;

import com.wotr.strategy.action.ActionResolverStrategy;
import com.wotr.strategy.action.MeleeActionResolverStrategy;
import com.wotr.strategy.action.RangedActionResolverStrategy;

public class ActionResolverFactory {

	public static ActionResolverStrategy getMeleeActionResolverStrategy() {
		return new MeleeActionResolverStrategy();
	}

	public static ActionResolverStrategy getRangedActionResolverStrategy() {
		return new RangedActionResolverStrategy();
	}
}
