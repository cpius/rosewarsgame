package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;

public class DefaultAttackStrategy implements AttackStrategy {

	@Override
	public boolean attack(BattleListener listener, DiceStrategy dice, Unit attackingUnit, Unit defendingUnit) {
		listener.attackStarted();

		int attackRoll = dice.roll();

		boolean attackSuccess = performAttack(attackRoll, attackingUnit, defendingUnit);
		if (attackSuccess) {
			listener.attackSuccessful(attackRoll);
		} else {
			listener.attackFailed(attackRoll);
		}
		return attackSuccess;
	}

	protected boolean performAttack(int attackRoll, Unit attackingUnit, Unit defendingUnit) {
		return attackRoll >= attackingUnit.getAttack();
	}
}
