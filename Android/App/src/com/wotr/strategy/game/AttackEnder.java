package com.wotr.strategy.game;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public interface AttackEnder {

	void endAttack(Unit attackingUnit, Position endPosition, boolean positionMoved);

}
