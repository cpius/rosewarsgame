package com.wotr.strategy.game.exceptions;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public class InvalidMoveException extends InvalidActionException {
	private static final long serialVersionUID = 1L;

	public InvalidMoveException(Unit movingUnit, Position newPosition) {
	}

}
