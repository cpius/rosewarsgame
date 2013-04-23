package com.wotr.model;

import com.wotr.model.unit.Unit;

public class AttackAction extends Action {

	public AttackAction(Unit unit, Position pos, ActionPath path) {
		super(unit, pos, path);
	}
	
	public AttackAction(Position position) {
		super(null, position, null);
	}
}
