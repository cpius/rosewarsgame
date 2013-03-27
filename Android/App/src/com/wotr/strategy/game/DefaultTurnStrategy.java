package com.wotr.strategy.game;

import java.util.ArrayList;

import com.wotr.model.unit.Unit;

public class DefaultTurnStrategy implements TurnStrategy {

	private int remainingActions = 1;
	private ArrayList<Unit> hasMoved = new ArrayList<Unit>();
	private ArrayList<Unit> hasAttacked = new ArrayList<Unit>();

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
	public void attack(Unit attackingUnit) {
		hasAttacked.add(attackingUnit);
		remainingActions -= attackingUnit.getActionsUsedForAttack();
	}

	@Override
	public void move(Unit movingUnit) {
		hasMoved.add(movingUnit);
		remainingActions--;
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
