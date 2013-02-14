package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public abstract class AbstractActionResolverStrategy implements ActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return !attackingUnits.containsKey(pos) && !defendingUnits.containsKey(pos);
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return defendingUnits.containsKey(pos);
	}

	@Override
	public int getPathLength(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		// TODO Add bonus points
		return Math.max(unit.getMovement(), unit.getRange());
	}

	public Direction[] getDirections(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		// TODO Implement ZOC movement rules
		return Direction.allDirections;
	}
}
