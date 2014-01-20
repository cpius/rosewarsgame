package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;

public interface BattleListener {

	void attackStarted(Unit attacker, Unit defender);

	void attackSuccessful(Unit attacker, Unit defender, int attackRoll);

	void attackFailed(Unit attacker, Unit defender, int attackRoll);

	void defenceStarted(Unit attacker, Unit defender);

	void defenceSuccessful(Unit attacker, Unit defender, int defenceRoll);

	void defenceFailed(Unit attacker, Unit defender, int defenceRoll);

}
