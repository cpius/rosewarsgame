package com.wotr.model;

import com.wotr.model.unit.Unit;

public class AttackAction extends Action {

	private Unit defendingUnit;

	public AttackAction(Unit attackingUnit, Unit defendingUnit, ActionPath path) {
		super(attackingUnit, defendingUnit.getPosition(), path);
		this.defendingUnit = defendingUnit;
	}
	
	public AttackAction(Position pos) {
		super(null, pos, null);		
	}
	
	public Unit getDefendingUnit() {
		return defendingUnit;
	}
	
}
