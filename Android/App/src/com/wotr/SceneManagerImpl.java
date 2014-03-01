package com.wotr;

import org.cocos2d.layers.CCScene;
import org.cocos2d.nodes.CCDirector;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;

import com.google.android.gms.games.multiplayer.turnbased.TurnBasedMatch;
import com.google.example.games.basegameutils.GameHelper;
import com.wotr.cocos.AbstractGameLayer;
import com.wotr.cocos.GameMenuLayer;
import com.wotr.strategy.game.AIGame;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.GoogleTurnbasedMatchGame;
import com.wotr.strategy.game.MultiplayerGame;

public class SceneManagerImpl implements SceneManager, GameMenuListener {

	private Context context;
	private Activity activity;
	private GameHelper mHelper;
	private GameMenuLayer gameMenuLayer;
	private BackListener backListener;

	public SceneManagerImpl(Activity activity, GameHelper mHelper) {
		this.activity = activity;
		this.mHelper = mHelper;
		this.context = activity.getApplicationContext();
	}

	@Override
	public void onAchievementsClicked() {
		activity.runOnUiThread(new Runnable() {
			public void run() {
				activity.startActivityForResult(mHelper.getGamesClient().getAchievementsIntent(), REQUEST_ACHIEVEMENTS);
			}
		});
	}

	@Override
	public void onLeaderboardButtonClicked() {
		activity.runOnUiThread(new Runnable() {
			public void run() {
				activity.startActivityForResult(mHelper.getGamesClient().getAllLeaderboardsIntent(), REQUEST_LEADERBOARD);
			}
		});

	}

	@Override
	public void onMultiplayerOnlineClicked() {
		activity.runOnUiThread(new Runnable() {
			public void run() {
				Intent selectPlayersIntent = mHelper.getGamesClient().getSelectPlayersIntent(1, 1);
				activity.startActivityForResult(selectPlayersIntent, REQUEST_SELECTPLAYERS);
			}
		});
	}

	@Override
	public void onMultiplayerLocalClicked() {

		activity.runOnUiThread(new Runnable() {
			public void run() {
				Game aiGame = new MultiplayerGame();
				showMatch(aiGame);
			}
		});

	}

	@Override
	public void onBotvsBotClicked() {
		activity.runOnUiThread(new Runnable() {
			public void run() {
				Game aiGame = new AIGame();
				showMatch(aiGame);
			}
		});
	}

	@Override
	public void onShowMachesClicked() {

		activity.runOnUiThread(new Runnable() {
			public void run() {
				Intent inbox = mHelper.getGamesClient().getMatchInboxIntent();
				activity.startActivityForResult(inbox, REQUEST_MATCHINBOX);
			}
		});
	}

	@Override
	public void showMainMenu(boolean signedIn) {

		backListener = null;

		LayerFactory factory = new LayerFactory(context, this);
		gameMenuLayer = factory.createGameMenuLayer(this);
		CCScene scene = CCScene.node();
		scene.addChild(gameMenuLayer);
		CCDirector.sharedDirector().runWithScene(scene);

		gameMenuLayer.enableLogin(!signedIn);

	}

	@Override
	public void onSignInButtonClicked() {
		activity.runOnUiThread(new Runnable() {
			public void run() {
				mHelper.beginUserInitiatedSignIn();
			}
		});
	}

	@Override
	public void onSignOutButtonClicked() {
		activity.runOnUiThread(new Runnable() {
			public void run() {
				mHelper.signOut();
				gameMenuLayer.enableLogin(true);
			}
		});
	}

	@Override
	public void showGoogleTurnbasedMatchGame(TurnBasedMatch match) {
		Game game = new GoogleTurnbasedMatchGame(mHelper, match);
		showMatch(game);
	}

	@Override
	public void showMatch(Game game) {

		boolean isSetup = game.isSetup();

		CCScene scene = CCScene.node();

		LayerFactory factory = new LayerFactory(context, this);

		if (isSetup) {
			AbstractGameLayer layer = factory.createPlayGameLayer(game);
			backListener = layer;
			scene.addChild(layer);
		} else {
			AbstractGameLayer layer = factory.createSetupGameLayer(game);
			backListener = layer;
			scene.addChild(layer);
		}

		CCDirector.sharedDirector().runWithScene(scene);

	}

	@Override
	public boolean backPressed() {
		if (backListener != null) {
			return backListener.backPressed(this);
		}

		return false;
	}

}
