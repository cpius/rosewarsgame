package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;

public interface AttackStrategy {

	boolean attack(BattleListener listener, DiceStrategy dice, Unit attackingUnit, Unit defendingUnit);

}
