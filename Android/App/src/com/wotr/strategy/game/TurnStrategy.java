package com.wotr.strategy.game;

import com.wotr.model.unit.Unit;

public interface TurnStrategy {

	int getRemainingActions();

	boolean canAttack(Unit attackingUnit);
	
	boolean canMove(Unit attackingUnit);

	void attacked(Unit attackingUnit);

	void moved(Unit movingUnit);

	int resetTurn();
	
	void resetGame();

	

}
