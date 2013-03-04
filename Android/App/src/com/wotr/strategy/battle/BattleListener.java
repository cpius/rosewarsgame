package com.wotr.strategy.battle;

public interface BattleListener {

	void attackStarted();

	void attackSuccessful(int attackRoll);

	void attackFailed(int attackRoll);

	void defenceStarted();

	void defenceSuccessful(int attackRoll);

	void defenceFailed(int attackRoll);

}
