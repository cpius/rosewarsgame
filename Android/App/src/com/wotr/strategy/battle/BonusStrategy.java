package com.wotr.strategy.battle;

import java.util.List;

import com.wotr.model.unit.Unit;

public interface BonusStrategy {

	void initializeDeck(List<Unit> deck);

	int getAttackWithBonus(Unit attackingUnit, Unit defendingUnit);
	
	int getDefenceWithBonus(Unit attackingUnit, Unit defendingUnit);
	

}
