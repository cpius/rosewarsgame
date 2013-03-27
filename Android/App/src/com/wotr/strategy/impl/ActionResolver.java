package com.wotr.strategy.impl;

import java.util.Collection;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

import com.wotr.GameManager;
import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.Direction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.action.ActionResolverStrategy;
import com.wotr.strategy.game.TurnStrategy;

public class ActionResolver {

	private final int yRange;
	private final int xRange;

	public ActionResolver(int xRange, int yRange) {
		this.yRange = yRange;
		this.xRange = xRange;
	}

	public Collection<Action> getActions(Unit originalunit, Map<Position, Unit> aUnits, Map<Position, Unit> dUnits) {
		TurnStrategy turnStrategy = GameManager.getFactory().getTurnStrategy();	
		
		
		ActionResolverStrategy actionResolverStrategy = originalunit.getActionResolverStrategy();
		return getActions(originalunit, originalunit.getPosistion(), null, true, aUnits, dUnits, 0, actionResolverStrategy, turnStrategy);
	}

	private Set<Action> getActions(Unit originalunit, Position pos, Direction lastDirection, boolean moveable, Map<Position, Unit> aUnits, Map<Position, Unit> dUnits, int pathProgress, ActionResolverStrategy ars, TurnStrategy turnStrategy) {

		Set<Action> moves = new HashSet<Action>();

		int pathLength = ars.getPathLength(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress);
		if (pathProgress < pathLength + 1) {

			if (!originalunit.getPosistion().equals(pos)) {

				if (ars.isAttackable(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress, turnStrategy)) {
					moves.add(new AttackAction(pos));
				} else if (moveable = ars.isMoveable(originalunit, pos, lastDirection, moveable, aUnits, dUnits, pathProgress, turnStrategy)) {
					moves.add(new MoveAction(pos));
				}
			}

			Collection<Direction> directions = ars.getDirections(originalunit, pos, lastDirection, aUnits, dUnits, pathProgress);
			for (Direction direction : directions) {
				Position movePosition = pos.move(direction);
				if (isInBoard(movePosition)) {
					moves.addAll(getActions(originalunit, movePosition, direction, moveable, aUnits, dUnits, pathProgress + 1, ars, turnStrategy));
				}
			}
		}

		return moves;
	}

	private boolean isInBoard(Position movedPosition) {
		return movedPosition.getX() >= 0 && movedPosition.getY() >= 0 && movedPosition.getX() < xRange && movedPosition.getY() < yRange;
	}
}
