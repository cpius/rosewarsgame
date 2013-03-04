package com.wotr;

import com.wotr.strategy.facade.DefaultGameFactory;
import com.wotr.strategy.facade.GameFactory;

public class GameManager {

	private static GameFactory factory = null;

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
}
