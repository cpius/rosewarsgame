package com.wotr.model;

import java.util.Collection;

import com.wotr.model.attack.AttackEndPosition;
import com.wotr.model.unit.attribute.bonus.BonusAward;

public class AttackResult {

	private final boolean succes;
	private final Collection<BonusAward> awardProspects;
	private Collection<AttackEndPosition> endPositions;

	public AttackResult(boolean succes, Collection<BonusAward> awardProspects, Collection<AttackEndPosition> endPositions) {
		this.succes = succes;
		this.awardProspects = awardProspects;
		this.endPositions = endPositions;

		for (AttackEndPosition attackEndPosition : endPositions) {
			attackEndPosition.setAttackResult(this);
		}
	}

	public boolean isSuccesfull() {
		return succes;
	}

	public Collection<AttackEndPosition> getEndPositionProspects() {
		return endPositions;
	}

	public Collection<BonusAward> getAwardProspects() {
		return awardProspects;
	}

	public AttackEndPosition getAttackEndPosition() {
		for (AttackEndPosition attackEndPosition : endPositions) {
			return attackEndPosition;
		}
		return null;
	}
}
