package com.wotr.strategy.battle.test;

import com.wotr.strategy.battle.BattleListener;

public class TestBattleListener implements BattleListener {

	int i;

	@Override
	public void attackStarted() {
		i += 1;
	}

	@Override
	public void attackSuccessful(int attackRoll) {
		i += 10;
	}

	@Override
	public void attackFailed(int attackRoll) {
		i += 100;
	}

	@Override
	public void defenceStarted() {
		i += 1000;
	}

	@Override
	public void defenceSuccessful(int attackRoll) {
		i += 10000;
	}

	@Override
	public void defenceFailed(int attackRoll) {
		i += 100000;
	}

	public int getObservations() {
		return i;
	}
}
