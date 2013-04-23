package com.wotr.strategy.factory;

import com.wotr.strategy.action.UnitActionResolverStrategy;
import com.wotr.strategy.action.MeleeActionResolverStrategy;
import com.wotr.strategy.action.RangedActionResolverStrategy;
import com.wotr.strategy.action.UnitTypeZocBlockStrategy;
import com.wotr.strategy.action.ZocBlockStrategy;

public class ActionResolverFactory {

	private static ZocBlockStrategy ZocBlockStrategy = null;

	public static void setZocBlockStrategy(ZocBlockStrategy zocBlockStrategy) {
		ZocBlockStrategy = zocBlockStrategy;
	}

	public static UnitActionResolverStrategy getMeleeActionResolverStrategy() {
		return new MeleeActionResolverStrategy();
	}

	public static UnitActionResolverStrategy getRangedActionResolverStrategy() {
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
