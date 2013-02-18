package com.wotr.strategy.action;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.facade.ActionResolverFactory;

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

	public Collection<Direction> getDirections(Unit unit, Position pos, Direction direction, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		List<Direction> result = new ArrayList<Direction>();
		ZocBlockStrategy zbs = ActionResolverFactory.getZocBlockStrategy();

		for (Direction d : Direction.perpendicularDirections) {
			if (!zbs.isDirectionBlocked(unit, d, pos, attackingUnits, defendingUnits)) {
				result.add(d);
				result.add(d.opposite());
			}
		}
		return result;
	}
}
