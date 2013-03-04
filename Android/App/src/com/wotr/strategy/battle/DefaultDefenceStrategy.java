package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;

public class DefaultDefenceStrategy implements DefenceStrategy {

	@Override
	public boolean defend(BattleListener listener, DiceStrategy dice, Unit attackingUnit, Unit defendingUnit) {
		listener.defenceStarted();

		int defenceRoll = dice.roll();

		boolean defenceSuccess = defenceRoll <= defendingUnit.getDefense();

		if (defenceSuccess) {
			listener.defenceSuccessful(defenceRoll);
		} else {
			listener.defenceFailed(defenceRoll);
		}
		return defenceSuccess;
	}
}
