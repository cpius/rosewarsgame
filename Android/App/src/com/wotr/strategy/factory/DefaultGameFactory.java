package com.wotr.strategy.factory;

import com.wotr.strategy.DiceStrategy;
import com.wotr.strategy.battle.AttackStrategy;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.battle.DefaultAttackStrategy;
import com.wotr.strategy.battle.DefaultBattleStrategy;
import com.wotr.strategy.battle.DefaultDefenceStrategy;
import com.wotr.strategy.battle.DefenceStrategy;
import com.wotr.strategy.battle.unit.ArcherAttackStrategy;
import com.wotr.strategy.battle.unit.PikemanAttackStrategy;
import com.wotr.strategy.game.DefaultTurnStrategy;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.TurnStrategy;
import com.wotr.strategy.impl.Random6DiceStrategy;

public class DefaultGameFactory implements GameFactory {

	private BattleStrategy battleStrategy;
	private DefaultTurnStrategy turnStrategy;
	private final Game game;

	public DefaultGameFactory(Game game) {
		this.game = game;
	}

	public BattleStrategy getBattleStrategy() {

		if (battleStrategy == null) {
			battleStrategy = new DefaultBattleStrategy();
		}
		return battleStrategy;
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

	public TurnStrategy getTurnStrategy() {
		if (turnStrategy == null) {
			turnStrategy = new DefaultTurnStrategy(game);
		}
		return turnStrategy;
	}
}
