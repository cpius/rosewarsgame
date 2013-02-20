package com.wotr.strategy.battle;

import com.wotr.GameManager;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;

public class DefaultBattleStrategy implements BattleStrategy {

	private BattleListener listener;

	@Override
	public boolean battle(Unit attackingUnit, Unit defendingUnit) {

		DiceStrategy dice = GameManager.getFactory().getDiceStrategy();

		boolean attackSucceded = attackingUnit.getAttackStrategy().attack(listener, dice, attackingUnit, defendingUnit);
		if (attackSucceded) {
			return !defendingUnit.getDefenceStrategy().defend(listener, dice, attackingUnit, defendingUnit);
		} else {
			return false;
		}
	}

	@Override
	public void addBattleListener(BattleListener listener) {
		this.listener = listener;
	}
}
