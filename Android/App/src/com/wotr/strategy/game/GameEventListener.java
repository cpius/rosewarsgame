package com.wotr.strategy.game;

import com.wotr.strategy.player.Player;

public interface GameEventListener {

	public void gameStarted();
	
	public void gameEnded(Player winner, Player looser);

	public void startTurn(Player player, int remainingActions);

	public void actionPerformed(Player player, int remainingActions);

	public void endTurn(Player player);

}
