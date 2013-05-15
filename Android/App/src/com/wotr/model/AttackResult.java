package com.wotr.model;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import com.wotr.model.unit.Unit;
import com.wotr.model.unit.attribute.bonus.BonusAward;
import com.wotr.strategy.game.AttackEnder;
import com.wotr.strategy.game.exceptions.InvalidEndPositionException;

public class AttackResult {

	private final boolean succes;
	private final List<Position> endPositions;
	private final Unit attackingUnit;
	private final AttackEnder attackEnder;
	private final Collection<BonusAward> awardProspects;

	public AttackResult(AttackEnder attackEnder, Unit attackingUnit, boolean succes, Position position, Collection<BonusAward> awardProspects) {
		this.attackEnder = attackEnder;
		this.attackingUnit = attackingUnit;
		this.succes = succes;
		this.awardProspects = awardProspects;

		endPositions = new ArrayList<Position>(1);
		endPositions.add(position);
	}

	public AttackResult(AttackEnder attackEnder, Unit attackingUnit, boolean succes, List<Position> endPositions, Collection<BonusAward> awardProspects) {
		this.attackEnder = attackEnder;
		this.attackingUnit = attackingUnit;
		this.succes = succes;
		this.endPositions = endPositions;
		this.awardProspects = awardProspects;
	}

	public boolean isSuccesfull() {
		return succes;
	}

	public List<Position> getEndPositions() {
		return endPositions;
	}

	public void endAttackAt(Position endPosition) throws InvalidEndPositionException {
		if (!endPositions.contains(endPosition)) {
			throw new InvalidEndPositionException();
		}

		attackEnder.endAttack(attackingUnit, endPosition);
		endPositions.clear();
	}

	public Collection<BonusAward> getAwardProspects() {
		return awardProspects;
	}
}
