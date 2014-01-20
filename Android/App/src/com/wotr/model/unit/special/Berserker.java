package com.wotr.model.unit.special;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;
import com.wotr.strategy.action.UnitActionResolverStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;

public class Berserker extends MeleeUnit {

	public Berserker() {
		super("special/berserker", false);
	}

	@Override
	public int getAttack() {
		return 2;
	}

	@Override
	public int getDefence() {
		return 1;
	}

	@Override
	public int getMovement() {
		return 1;
	}

	@Override
	public int getRange() {
		return 1;
	}

	@Override
	public UnitType getType() {
		return UnitType.INFANTRY;
	}
	
	@Override
	public UnitActionResolverStrategy getActionResolverStrategy() {
		return ActionResolverFactory.getBerserkerActionResolverStrategy();
	}
}
