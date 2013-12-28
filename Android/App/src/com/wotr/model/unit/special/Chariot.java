package com.wotr.model.unit.special;

import com.wotr.model.UnitType;
import com.wotr.model.unit.MeleeUnit;
import com.wotr.strategy.battle.AttackEndpointResolverStrategy;
import com.wotr.strategy.battle.unit.ChariotAttackEndpointResolverStrategy;
import com.wotr.strategy.game.Game;

public class Chariot extends MeleeUnit {

	public Chariot() {
		super("special/chariot", false);
	}

	@Override
	public int getAttack() {
		return 4;
	}

	@Override
	public int getDefence() {
		return 3;
	}

	@Override
	public int getMovement() {
		return 3;
	}

	@Override
	public int getRange() {
		return 1;
	}

	@Override
	public UnitType getType() {
		return UnitType.CAVALRY;
	}
	
	@Override
	public AttackEndpointResolverStrategy getAttackEndpointResolverStrategy(Game game) {
		return new ChariotAttackEndpointResolverStrategy(this, game);
	}
}
