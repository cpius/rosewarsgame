package com.wotr.strategy.game;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.player.Player;

public interface Game {

	void startGame();
	
	Player getAttackingPlayer();
	
	Player getDefendingPlayer();
	
	void addGameEventListener(GameEventListener listener);
	
	boolean attack(Unit attackingUnit, Unit defendingUnit);
	
	void move(Position oldPosition, Position newPosition);
}
