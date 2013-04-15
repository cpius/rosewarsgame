package com.wotr.strategy.battle;

import java.util.List;

import com.wotr.model.unit.Unit;

public class DefaultBonusStrategy implements BonusStrategy {

	@Override
	public void initializeDeck(List<Unit> deck) {
		deck.get(0).addAttackBonus();
		deck.get(1).addDefenceBonus();
	}

	@Override
	public int getAttackWithBonus(Unit attackingUnit, Unit defendingUnit) {
		return attackingUnit.getAttackWithUnitBonus();
	}

	@Override
	public int getDefenceWithBonus(Unit attackingUnit, Unit defendingUnit) {
		return defendingUnit.getDefenseWithUnitBonus();
	}
}
