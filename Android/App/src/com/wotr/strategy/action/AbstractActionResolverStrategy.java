package com.wotr.strategy.action;

import java.util.Arrays;
import java.util.Collection;
import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.TurnStrategy;

public abstract class AbstractActionResolverStrategy implements ActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, Direction direction, boolean movable, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		
		if(!turnStrategy.canMove(unit)) {
			return false;
		}
		
		return movable && !attackingUnits.containsKey(pos) && !defendingUnits.containsKey(pos);
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		
		if(!turnStrategy.canAttack(unit)) {
			return false;
		}
		
		return defendingUnits.containsKey(pos);
	}

	@Override
	public int getPathLength(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		// TODO Add bonus points
		return Math.max(unit.getMovement(), unit.getRange());
	}

	public Collection<Direction> getDirections(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return Arrays.asList(Direction.allDirections);
	}
}
