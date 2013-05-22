package com.wotr.model;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import com.wotr.model.attack.AttackEndPosition;
import com.wotr.model.unit.attribute.bonus.BonusAward;

public class AttackResult {

	private final boolean succes;
	private final List<AttackEndPosition> endPositions = new ArrayList<AttackEndPosition>();
	private final Collection<BonusAward> awardProspects;

	public AttackResult(boolean succes, Collection<BonusAward> awardProspects) {
		this.succes = succes;
		this.awardProspects = awardProspects;
	}

	public boolean isSuccesfull() {
		return succes;
	}

	public List<AttackEndPosition> getEndPositionProspects() {
		return endPositions;
	}

	public Collection<BonusAward> getAwardProspects() {
		return awardProspects;
	}

	public void addEndposition(AttackEndPosition attackEndPosition) {
		endPositions.add(attackEndPosition);
		attackEndPosition.setAttackResult(this);
	}
}
