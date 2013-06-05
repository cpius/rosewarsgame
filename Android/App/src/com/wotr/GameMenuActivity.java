package com.wotr;

import org.cocos2d.layers.CCScene;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.opengl.CCGLSurfaceView;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Window;
import android.view.WindowManager;

import com.google.example.games.basegameutils.GameHelper;
import com.google.example.games.basegameutils.GameHelper.GameHelperListener;
import com.wotr.cocos.GameMenuLayer;
import com.wotr.cocos.SetupGameLayer;

public class GameMenuActivity extends Activity implements GameMenuListener, GameHelperListener {

	protected static final int REQUEST_ACHIEVEMENTS = 0;
	protected static final int REQUEST_LEADERBOARD = 1;
	protected static final int REQUEST_SELECTPLAYERS = 2;
	private CCGLSurfaceView _glSurfaceView;
	private GameHelper mHelper;
	private GameMenuLayer gameMenuLayer;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		requestWindowFeature(Window.FEATURE_NO_TITLE);
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON, WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

		_glSurfaceView = new CCGLSurfaceView(this);
		setContentView(_glSurfaceView);

		mHelper = new GameHelper(this);
		mHelper.setup(this);
	}

	@Override
	public void onStart() {
		super.onStart();
		CCDirector.sharedDirector().attachInView(_glSurfaceView);
		CCDirector.sharedDirector().setDisplayFPS(true);
		CCDirector.sharedDirector().setAnimationInterval(1.0f / 60.0f);

		gameMenuLayer = new GameMenuLayer(this);

		CCScene scene = CCScene.node();
		scene.addChild(gameMenuLayer);
		CCDirector.sharedDirector().runWithScene(scene);

		mHelper.onStart(this);
	}

	@Override
	public void onPause() {
		super.onPause();
		CCDirector.sharedDirector().pause();
	}

	@Override
	public void onResume() {
		super.onResume();
		CCDirector.sharedDirector().resume();
	}

	@Override
	public void onStop() {
		super.onStop();
		CCDirector.sharedDirector().end();
		mHelper.onStop();
	}

	@Override
	protected void onActivityResult(int request, int response, Intent data) {
		super.onActivityResult(request, response, data);
		mHelper.onActivityResult(request, response, data);
	}

	@Override
	public void onSignInButtonClicked() {
		runOnUiThread(new Runnable() {
			public void run() {
				mHelper.beginUserInitiatedSignIn();
			}
		});
	}

	@Override
	public void onSignOutButtonClicked() {
		runOnUiThread(new Runnable() {
			public void run() {
				mHelper.signOut();
				gameMenuLayer.enableLogin(true);
			}
		});

	}

	@Override
	public void onSignInFailed() {
		gameMenuLayer.enableLogin(true);
	}

	@Override
	public void onSignInSucceeded() {
		gameMenuLayer.enableLogin(false);
	}

	@Override
	public void onAchievementsClicked() {
		runOnUiThread(new Runnable() {
			public void run() {
				startActivityForResult(mHelper.getGamesClient().getAchievementsIntent(), REQUEST_ACHIEVEMENTS);
			}
		});
	}

	@Override
	public void onLeaderboardButtonClicked() {
		runOnUiThread(new Runnable() {
			public void run() {
				startActivityForResult(mHelper.getGamesClient().getAllLeaderboardsIntent(), REQUEST_LEADERBOARD);
			}
		});

	}

	@Override
	public void onMultiplayerOnlineClicked() {
		runOnUiThread(new Runnable() {
			public void run() {
				startActivityForResult(mHelper.getGamesClient().getSelectPlayersIntent(1, 2), REQUEST_SELECTPLAYERS);
			}
		});
	}

	@Override
	public void onMultiplayerLocalClicked() {

		runOnUiThread(new Runnable() {
			public void run() {

				CCScene scene = SetupGameLayer.scene();
				CCDirector.sharedDirector().runWithScene(scene);

				 /*Intent myIntent = new Intent(getApplicationContext(),
				 SetupGameActivity.class);
				 startActivityForResult(myIntent, 0);*/
			}
		});

	}
}
