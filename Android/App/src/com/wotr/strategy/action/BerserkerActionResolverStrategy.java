package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.ActionPath;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.TurnStrategy;

public class BerserkerActionResolverStrategy extends MeleeActionResolverStrategy implements UnitActionResolverStrategy {

	private static final int BERSERK_ATTACKRANGE = 4;

	@Override
	/**
	 * if attacking position is within 4 tiles from the berserker, attack is possible
	 */
	public boolean isAttackable(Unit unit, Position pos, ActionPath path, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress, TurnStrategy turnStrategy) {
		return turnStrategy.canAttack(unit) && defendingUnits.containsKey(pos) && pathProgress <= BERSERK_ATTACKRANGE;
	}

	@Override
	public int getPathLength(Unit unit, Position pos, ActionPath path, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits, int pathProgress) {
		return Math.max(super.getPathLength(unit, pos, path, attackingUnits, defendingUnits, pathProgress), BERSERK_ATTACKRANGE);
	}
}
