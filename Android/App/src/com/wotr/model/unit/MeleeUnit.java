package com.wotr.model.unit;

import com.wotr.strategy.action.UnitActionResolverStrategy;
import com.wotr.strategy.battle.AttackEndpointResolverStrategy;
import com.wotr.strategy.battle.unit.MeleeAttackEndpointResolverStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;

public abstract class MeleeUnit extends Unit {

	public MeleeUnit(String image, boolean enemy) {
		super(image, enemy);
	}

	public boolean isRanged() {
		return false;
	}

	@Override
	public UnitActionResolverStrategy getActionResolverStrategy() {
		return ActionResolverFactory.getMeleeActionResolverStrategy();
	}

	@Override
	public AttackEndpointResolverStrategy getAttackEndpointResolverStrategy() {
		return new MeleeAttackEndpointResolverStrategy(this);
	}
}
