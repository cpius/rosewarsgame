package com.wotr.strategy.factory;

import com.wotr.strategy.action.ActionResolverStrategy;
import com.wotr.strategy.action.MeleeActionResolverStrategy;
import com.wotr.strategy.action.RangedActionResolverStrategy;
import com.wotr.strategy.action.UnitTypeZocBlockStrategy;
import com.wotr.strategy.action.ZocBlockStrategy;

public class ActionResolverFactory {

	private static ZocBlockStrategy ZocBlockStrategy = null;

	public static void setZocBlockStrategy(ZocBlockStrategy zocBlockStrategy) {
		ZocBlockStrategy = zocBlockStrategy;
	}

	public static ActionResolverStrategy getMeleeActionResolverStrategy() {
		return new MeleeActionResolverStrategy();
	}

	public static ActionResolverStrategy getRangedActionResolverStrategy() {
		return new RangedActionResolverStrategy();
	}

	public static ZocBlockStrategy getZocBlockStrategy() {
		if (ZocBlockStrategy != null) {
			return ZocBlockStrategy;
		}
		ZocBlockStrategy = new UnitTypeZocBlockStrategy();
		return ZocBlockStrategy;
	}
}
