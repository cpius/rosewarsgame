package com.wotr.strategy.game;

import com.wotr.model.Action;
import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.player.Player;

public class AIGame implements Game {

	@Override
	public void startGame() {
		// TODO Auto-generated method stub

	}

	@Override
	public Player getAttackingPlayer() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public Player getDefendingPlayer() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void addGameEventListener(GameEventListener listener) {
		// TODO Auto-generated method stub

	}

	@Override
	public AttackResult attack(Action action, Unit defendingUnit) {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public void move(Unit movingUnit, Position movingPosistion) {
		// TODO Auto-generated method stub

	}

	@Override
	public void setActionsResolver(ActionsResolverStrategy actionsResolver) {
		// TODO Auto-generated method stub
		
	}

}
