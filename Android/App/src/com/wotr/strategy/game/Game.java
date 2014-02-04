package com.wotr.strategy.game;

import com.wotr.model.Action;
import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.game.exceptions.InvalidAttackException;
import com.wotr.strategy.game.exceptions.InvalidMoveException;
import com.wotr.strategy.player.Player;

public interface Game {

	void startGame();

	Player getAttackingPlayer();

	Player getDefendingPlayer();

	void addGameEventListener(GameEventListener listener);

	AttackResult attack(Action action, Unit defendingUnit) throws InvalidAttackException;

	void move(Unit unit, Position newPosition) throws InvalidMoveException;

	void setActionsResolver(ActionsResolverStrategy actionsResolver);
	
	ActionsResolverStrategy getActionsResolver();

	boolean isSetup();

	int getXTileCount();

	int getYTileCount();

	void endAttack(Unit attackingUnit, Position endPosition, boolean moved);

	void setupDone(Player player);
	
	int getRemainingActions();

}
