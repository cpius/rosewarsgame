package com.wotr.model.attack;

import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public abstract class AbstractAttackEndPosition implements AttackEndPosition {

	private Position position;
	protected final Unit attackingUnit;
	private AttackResult attackResult;

	public AbstractAttackEndPosition(Unit attackingUnit, Position position) {
		this.attackingUnit = attackingUnit;
		this.position = position;
	}

	@Override
	public Position getPosition() {
		return position;
	}

	public abstract void endAttack();

	@Override
	public void setAttackResult(AttackResult attackResult) {
		this.attackResult = attackResult;
	}

	@Override
	public AttackResult getAttackResult() {
		return attackResult;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + ((attackingUnit == null) ? 0 : attackingUnit.hashCode());
		result = prime * result + ((position == null) ? 0 : position.hashCode());
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		AbstractAttackEndPosition other = (AbstractAttackEndPosition) obj;
		if (attackingUnit == null) {
			if (other.attackingUnit != null)
				return false;
		} else if (!attackingUnit.equals(other.attackingUnit))
			return false;
		if (position == null) {
			if (other.position != null)
				return false;
		} else if (!position.equals(other.position))
			return false;
		return true;
	}
	
	
	
	
}
