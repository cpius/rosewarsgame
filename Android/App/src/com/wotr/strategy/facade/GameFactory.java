
package com.wotr.strategy.facade;

import com.wotr.strategy.DiceStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.battle.DefenceStrategy;

public interface GameFactory {

	BattleStrategy getBattleStrategy();

	DiceStrategy getDiceStrategy();

	AttackStrategy getAttackStrategy();

	DefenceStrategy getDefenceStrategy();

	AttackStrategy getArcherAttackStrategy();

	AttackStrategy getPikemanAttackStrategy();

}
