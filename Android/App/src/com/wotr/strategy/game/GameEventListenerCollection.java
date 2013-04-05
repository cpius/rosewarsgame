package com.wotr.strategy.game;

import java.util.ArrayList;

import com.wotr.strategy.player.Player;

public class GameEventListenerCollection extends ArrayList<GameEventListener> implements GameEventListener {

	private static final long serialVersionUID = 1L;

	@Override
	public void gameStarted() {
		for (GameEventListener listener : this) {
			listener.gameStarted();
		}
	}

	@Override
	public void startTurn(Player player, int remainingActions) {
		for (GameEventListener listener : this) {
			listener.startTurn(player, remainingActions);
		}
	}

	@Override
	public void actionPerformed(Player player, int remainingActions) {
		for (GameEventListener listener : this) {
			listener.actionPerformed(player, remainingActions);
		}
	}

	@Override
	public void gameEnded(Player winner) {
		for (GameEventListener listener : this) {
			listener.gameEnded(winner);
		}		
	}
}
