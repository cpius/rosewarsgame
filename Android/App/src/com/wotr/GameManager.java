package com.wotr;

import com.wotr.strategy.factory.DefaultGameFactory;
import com.wotr.strategy.factory.GameFactory;
import com.wotr.strategy.game.Game;

public class GameManager {

	private static GameFactory factory = null;
	private static Game game;

	public static GameFactory setFactory(GameFactory factory) {
		GameManager.factory = factory;
		return factory;
	}

	public static GameFactory getFactory() {
		if (factory == null) {
			factory = new DefaultGameFactory();
		}
		return factory;
	}

	public static void setGame(Game game) {
		GameManager.game = game;
	}

	public static Game getGame() {
		return game;
	}

}
