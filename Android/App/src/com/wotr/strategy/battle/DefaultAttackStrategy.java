package com.wotr.strategy.battle;

import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;

public class DefaultAttackStrategy implements AttackStrategy {

	@Override
	public boolean attack(BattleListener listener, DiceStrategy dice, Unit attackingUnit, Unit defendingUnit) {
		listener.attackStarted(attackingUnit, defendingUnit);

		int attackRoll = dice.roll();

		boolean attackSuccess = performAttack(attackRoll, attackingUnit, defendingUnit);
		if (attackSuccess) {
			listener.attackSuccessful(attackingUnit, defendingUnit, attackRoll);
		} else {
			listener.attackFailed(attackingUnit, defendingUnit, attackRoll);
		}
		return attackSuccess;
	}

	protected boolean performAttack(int attackRoll, Unit attackingUnit, Unit defendingUnit) {
		return attackRoll >= getAttackWithBonus(attackingUnit, defendingUnit);
	}

	protected int getAttackWithBonus(Unit attackingUnit, Unit defendingUnit) {
		BonusStrategy bonusStrategy = attackingUnit.getBonusStrategy();
		return bonusStrategy.getAttackWithBonus(attackingUnit, defendingUnit);		
	}
}
