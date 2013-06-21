package com.wotr.model.unit;

import com.wotr.strategy.action.UnitActionResolverStrategy;
import com.wotr.strategy.battle.AttackEndpointResolverStrategy;
import com.wotr.strategy.battle.unit.RangedAttackEndpointResolverStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;

public abstract class RangedUnit extends Unit {

	public RangedUnit(String image, boolean enemy) {
		super(image, enemy);
	}

	public boolean isRanged() {
		return true;
	}

	@Override
	public UnitActionResolverStrategy getActionResolverStrategy() {
		return ActionResolverFactory.getRangedActionResolverStrategy();
	}	
	
	@Override
	public AttackEndpointResolverStrategy getAttackEndpointResolverStrategy() {
		return new RangedAttackEndpointResolverStrategy(this);
	}

	public String getAttackSound() {
		return "sounds/bow_attack.wav";
	}
}
