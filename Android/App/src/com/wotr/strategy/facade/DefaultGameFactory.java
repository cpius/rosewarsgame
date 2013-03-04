package com.wotr.strategy.facade;

import com.wotr.strategy.DiceStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.battle.DefaultAttackStrategy;
import com.wotr.strategy.battle.DefaultBattleStrategy;
import com.wotr.strategy.battle.DefaultDefenceStrategy;
import com.wotr.strategy.battle.DefenceStrategy;
import com.wotr.strategy.battle.unit.ArcherAttackStrategy;
import com.wotr.strategy.battle.unit.PikemanAttackStrategy;
import com.wotr.strategy.impl.Random6DiceStrategy;

public class DefaultGameFactory implements GameFactory {

	public BattleStrategy getBattleStrategy() {
		return new DefaultBattleStrategy();
	}

	public DiceStrategy getDiceStrategy() {
		return new Random6DiceStrategy();
	}

	public AttackStrategy getAttackStrategy() {
		return new DefaultAttackStrategy();
	}

	public DefenceStrategy getDefenceStrategy() {
		return new DefaultDefenceStrategy();
	}

	public AttackStrategy getArcherAttackStrategy() {
		return new ArcherAttackStrategy();
	}

	public AttackStrategy getPikemanAttackStrategy() {
		return new PikemanAttackStrategy();
	}
}
