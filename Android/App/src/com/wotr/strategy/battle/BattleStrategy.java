package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;

public interface BattleStrategy {

	boolean battle(Unit attackingUnit, Unit defendingUnit);

	void addBattleListener(BattleListener listener);

}
