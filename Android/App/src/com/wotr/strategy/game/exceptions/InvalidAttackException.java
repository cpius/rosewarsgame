package com.wotr.strategy.game.exceptions;

import com.wotr.model.unit.Unit;

public class InvalidAttackException extends InvalidActionException {

	private static final long serialVersionUID = 1L;

	public InvalidAttackException(Unit attackingUnit, Unit defendingUnit) {
	}
}
