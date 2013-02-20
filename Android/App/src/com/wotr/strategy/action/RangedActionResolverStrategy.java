package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public class RangedActionResolverStrategy extends AbstractActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, Direction direction, boolean moveable, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		
		//TODO Implement ZOC here
		
		return super.isMoveable(unit, pos, direction, moveable, attackingUnits, defendingUnits, pathProgress) && pathProgress <= unit.getMovement();
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return super.isAttackable(unit, pos, direction, attackingUnits, defendingUnits, pathProgress) && pathProgress <= unit.getRange();
	}
}
