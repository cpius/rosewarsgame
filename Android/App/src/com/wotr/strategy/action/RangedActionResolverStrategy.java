package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.ActionPath;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.TurnStrategy;

public class RangedActionResolverStrategy extends AbstractUnitActionResolverStrategy {

	@Override
	public boolean isMoveable(Unit unit, Position pos, ActionPath path, boolean moveable, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		
		//TODO Implement ZOC here
		
		return super.isMoveable(unit, pos, path, moveable, attackingUnits, defendingUnits, pathProgress, turnStrategy) && pathProgress <= unit.getMovement();
	}

	@Override
	public boolean isAttackable(Unit unit, Position pos, ActionPath path, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		return super.isAttackable(unit, pos, path, attackingUnits, defendingUnits, pathProgress, turnStrategy) && pathProgress <= unit.getRange();
	}
}
