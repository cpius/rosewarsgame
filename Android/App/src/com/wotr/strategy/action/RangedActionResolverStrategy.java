package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.TurnStrategy;

public class RangedActionResolverStrategy extends AbstractActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, Direction direction, boolean moveable, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		
		//TODO Implement ZOC here
		
		return super.isMoveable(unit, pos, direction, moveable, attackingUnits, defendingUnits, pathProgress, turnStrategy) && pathProgress <= unit.getMovement();
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		return super.isAttackable(unit, pos, direction, attackingUnits, defendingUnits, pathProgress, turnStrategy) && pathProgress <= unit.getRange();
	}
}
