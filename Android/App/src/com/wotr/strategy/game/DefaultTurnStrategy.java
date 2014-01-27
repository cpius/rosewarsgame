package com.wotr.strategy.game;

import java.util.ArrayList;
import java.util.Collection;

import com.wotr.model.unit.Unit;

public class DefaultTurnStrategy implements TurnStrategy {

	private int remainingActions = 1;
	private ArrayList<Unit> hasMoved = new ArrayList<Unit>();
	private ArrayList<Unit> hasAttacked = new ArrayList<Unit>();
	private final Game game;

	public DefaultTurnStrategy(Game game) {
		this.game = game;
	}

	@Override
	public int getRemainingActions() {
		return remainingActions;
	}

	@Override
	public boolean canAttack(Unit unit) {
		return remainingActions >= unit.getActionsUsedForAttack() && !hasUsedTurn(unit);
	}

	@Override
	public boolean canMove(Unit unit) {
		return remainingActions >= 1 && !hasUsedTurn(unit);
	}

	@Override
	public void attacked(Unit attackingUnit) {
		hasAttacked.add(attackingUnit);

		Collection<Unit> units = game.getAttackingPlayer().getUnitMap().values();
		if (units.size() == 1 && units.contains(attackingUnit)) {
			remainingActions = 0;
		} else {
			remainingActions -= attackingUnit.getActionsUsedForAttack();
		}
	}

	@Override
	public void moved(Unit movingUnit) {
		hasMoved.add(movingUnit);
		
		Collection<Unit> units = game.getAttackingPlayer().getUnitMap().values();
		if (units.size() == 1 && units.contains(movingUnit)) {
			remainingActions = 0;
		} else {
			remainingActions--;
		}
	}

	@Override
	public int resetTurn() {
		remainingActions = 2;
		hasAttacked.clear();
		hasMoved.clear();
		return remainingActions;
	}

	@Override
	public void resetGame() {
		resetTurn();
		remainingActions = 1;
	}

	boolean hasUsedTurn(Unit unit) {
		return hasAttacked.contains(unit) || hasMoved.contains(unit);
	}
}
