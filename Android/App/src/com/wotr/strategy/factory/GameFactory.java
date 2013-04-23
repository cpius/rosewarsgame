package com.wotr.strategy.factory;

import com.wotr.strategy.DiceStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.battle.BonusStrategy;
import com.wotr.strategy.battle.DefenceStrategy;
import com.wotr.strategy.game.TurnStrategy;

public interface GameFactory {

	BattleStrategy getBattleStrategy();

	DiceStrategy getDiceStrategy();

	AttackStrategy getAttackStrategy();

	DefenceStrategy getDefenceStrategy();

	AttackStrategy getArcherAttackStrategy();

	AttackStrategy getPikemanAttackStrategy();

	TurnStrategy getTurnStrategy();

	BonusStrategy getBonusStrategy();
}
