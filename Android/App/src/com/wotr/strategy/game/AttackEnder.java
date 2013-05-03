package com.wotr.strategy.game;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.exceptions.InvalidEndPosition;

public interface AttackEnder {
	
	void endAttack(Unit attackingUnit, Position endPosition) throws InvalidEndPosition;

}
