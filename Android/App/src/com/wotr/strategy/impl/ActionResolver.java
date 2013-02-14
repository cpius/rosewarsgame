package com.wotr.strategy.impl;

import java.util.Collection;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.Direction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.action.ActionResolverStrategy;

public class ActionResolver {

	private final int yRange;
	private final int xRange;

	public ActionResolver(int xRange, int yRange) {
		this.yRange = yRange;
		this.xRange = xRange;
	}

	public Collection<Action> getActions(Unit originalunit, Map<Position, Unit> aUnits, Map<Position, Unit> dUnits) {
		ActionResolverStrategy ars = originalunit.getActionResolverStrategy();
		return getActions(originalunit, originalunit.getPosistion(), null, aUnits, dUnits, 0, ars);
	}

	private Set<Action> getActions(Unit originalunit, Position pos, Direction lastDirection, Map<Position, Unit> aUnits, Map<Position, Unit> dUnits, int pathProgress, ActionResolverStrategy ars) {

		Set<Action> moves = new HashSet<Action>();

		int pathLength = ars.getPathLength(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress);
		if (pathProgress < pathLength + 1) {

			if (!originalunit.getPosistion().equals(pos)) {

				if (ars.isAttackable(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress)) {
					moves.add(new AttackAction(pos));
				} else if (ars.isMoveable(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress)) {
					moves.add(new MoveAction(pos));
				}
			}

			Direction[] directions = ars.getDirections(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress);
			for (Direction direction : directions) {
				Position movePosition = pos.move(direction);
				if (isInBoard(movePosition)) {
					moves.addAll(getActions(originalunit, movePosition, direction, aUnits, dUnits, pathProgress + 1, ars));
				}
			}
		}

		return moves;
	}

	private boolean isInBoard(Position movedPosition) {
		return movedPosition.getX() >= 0 && movedPosition.getY() >= 0 && movedPosition.getX() < xRange && movedPosition.getY() < yRange;
	}
}
