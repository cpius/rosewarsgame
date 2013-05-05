package com.wotr.model;

import java.util.ArrayList;
import java.util.List;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.game.AttackEnder;
import com.wotr.strategy.game.exceptions.InvalidEndPosition;

public class AttackResult {

	private final boolean succes;
	private final List<Position> endPositions;
	private final Unit attackingUnit;
	private final AttackEnder attackEnder;

	public AttackResult(AttackEnder attackEnder, Unit attackingUnit, boolean succes, Position position) {
		this.attackEnder = attackEnder;
		this.attackingUnit = attackingUnit;
		this.succes = succes;

		endPositions = new ArrayList<Position>(1);
		endPositions.add(position);
	}

	public AttackResult(AttackEnder attackEnder, Unit attackingUnit, boolean succes, List<Position> endPositions) {
		this.attackEnder = attackEnder;
		this.attackingUnit = attackingUnit;
		this.succes = succes;
		this.endPositions = endPositions;
	}

	public boolean isSuccesfull() {
		return succes;
	}

	public List<Position> getEndPositions() {
		return endPositions;
	}

	public void endAttackAt(Position endPosition) throws InvalidEndPosition {
		if (!endPositions.contains(endPosition)) {
			throw new InvalidEndPosition();
		}

		attackEnder.endAttack(attackingUnit, endPosition);
	}
}
