package com.wotr.strategy.battle.test;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.battle.BattleListener;

public class TestBattleListener implements BattleListener {

	int i;

	@Override
	public void attackStarted(Unit a, Unit d) {
		i += 1;
	}

	@Override
	public void attackSuccessful(Unit a, Unit d, int attackRoll) {
		i += 10;
	}

	@Override
	public void attackFailed(Unit a, Unit d, int attackRoll) {
		i += 100;
	}

	@Override
	public void defenceStarted(Unit a, Unit d) {
		i += 1000;
	}

	@Override
	public void defenceSuccessful(Unit a, Unit d, int attackRoll) {
		i += 10000;
	}

	@Override
	public void defenceFailed(Unit a, Unit d, int attackRoll) {
		i += 100000;
	}

	public int getObservations() {
		return i;
	}
}
