package com.wotr.model;

import com.wotr.model.unit.Unit;

public class MoveAction extends Action {

	public MoveAction(Unit unit, Position pos, ActionPath path) {
		super(unit, pos, path);
	}

	public MoveAction(Position position) {
		super(null, position, null);
	}
}
