package com.wotr;

import android.content.Context;

import com.wotr.cocos.AbstractGameLayer;
import com.wotr.cocos.GameMenuLayer;
import com.wotr.cocos.layout.flat.PlayGameLayerFlat;
import com.wotr.cocos.layout.flat.SetupGameLayerFlat;
import com.wotr.cocos.layout.perspective.PlayGameLayerPerspective;
import com.wotr.cocos.layout.perspective.SetupGameLayerPerspective;
import com.wotr.strategy.game.Game;

public class LayerFactory {

	private Context context;
	private SceneManager sceneManager;

	private boolean flat = true;

	public LayerFactory(Context context, SceneManager sceneManager) {
		this.context = context;
		this.sceneManager = sceneManager;
	}

	public AbstractGameLayer createPlayGameLayer(Game game) {

		if (flat) {
			return new PlayGameLayerFlat(context, sceneManager, game);
		} else {
			return new PlayGameLayerPerspective(context, sceneManager, game);
		}
	}

	public AbstractGameLayer createSetupGameLayer(Game game) {

		if (flat) {
			return new SetupGameLayerFlat(context, sceneManager, game);
		} else {
			return new SetupGameLayerPerspective(context, sceneManager, game);
		}
	}

	public GameMenuLayer createGameMenuLayer(GameMenuListener listeners) {
		return new GameMenuLayer(context, listeners);
	}
}
