package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;

public class DefaultDefenceStrategy implements DefenceStrategy {

	@Override
	public boolean defend(BattleListener listener, DiceStrategy dice, Unit attackingUnit, Unit defendingUnit) {
		listener.defenceStarted(attackingUnit, defendingUnit);

		int defenceRoll = dice.roll();

		boolean defenceSuccess = defenceRoll <= defendingUnit.getDefenceAttribute().calculateValue();

		if (defenceSuccess) {
			listener.defenceSuccessful(attackingUnit, defendingUnit, defenceRoll);
		} else {
			listener.defenceFailed(attackingUnit, defendingUnit, defenceRoll);
		}
		return defenceSuccess;
	}	
}
