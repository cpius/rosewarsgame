package com.wotr.strategy.action;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import com.wotr.model.ActionPath;
import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.factory.ActionResolverFactory;
import com.wotr.strategy.game.TurnStrategy;

public class MeleeActionResolverStrategy extends AbstractUnitActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, ActionPath path, boolean movable, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		return super.isMoveable(unit, pos, path, movable, attackingUnits, defendingUnits, pathProgress, turnStrategy) && pathProgress <= unit.getMovement();
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, ActionPath path, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		return super.isAttackable(unit, pos, path, attackingUnits, defendingUnits, pathProgress, turnStrategy) && pathProgress <= unit.getMovement();
	}

	@Override
	public Collection<Direction> getDirections(Unit unit, Position pos, ActionPath path, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {

		// If pos has any unit, Melee units will not be able to move or attack any further
		if (!unit.getPosition().equals(pos) && (attackingUnits.containsKey(pos) || defendingUnits.containsKey(pos))) {
			return Collections.emptyList();
		} else {
			return getZocDirections(unit, pos, path, attackingUnits, defendingUnits, pathProgress);
		}
	}

	private Collection<Direction> getZocDirections(Unit unit, Position pos, ActionPath path, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
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
