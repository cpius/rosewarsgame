package com.wotr;

import java.util.ArrayList;

import org.cocos2d.nodes.CCDirector;
import org.cocos2d.opengl.CCGLSurfaceView;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Window;
import android.view.WindowManager;

import com.google.android.gms.games.GamesClient;
import com.google.android.gms.games.multiplayer.realtime.RoomConfig;
import com.google.android.gms.games.multiplayer.turnbased.OnTurnBasedMatchInitiatedListener;
import com.google.android.gms.games.multiplayer.turnbased.OnTurnBasedMatchUpdatedListener;
import com.google.android.gms.games.multiplayer.turnbased.TurnBasedMatch;
import com.google.android.gms.games.multiplayer.turnbased.TurnBasedMatchConfig;
import com.google.example.games.basegameutils.GameHelper;
import com.google.example.games.basegameutils.GameHelper.GameHelperListener;

public class GameActivity extends Activity implements GameHelperListener, OnTurnBasedMatchInitiatedListener, OnTurnBasedMatchUpdatedListener {

	private CCGLSurfaceView _glSurfaceView;
	private GameHelper mHelper;

	private SceneManager sceneManager = null;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);

		requestWindowFeature(Window.FEATURE_NO_TITLE);
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
		getWindow().setFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON, WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);

		_glSurfaceView = new CCGLSurfaceView(this);
		setContentView(_glSurfaceView);

		mHelper = new GameHelper(this);
		mHelper.enableDebugLog(true, getClass().getName());
		mHelper.setup(this, GameHelper.CLIENT_GAMES | GameHelper.CLIENT_PLUS);

		sceneManager = new SceneManagerImpl(this, mHelper);

	}

	@Override
	public void onStart() {
		Log.i(getClass().getName(), "OnStart called");

		super.onStart();
		CCDirector.sharedDirector().attachInView(_glSurfaceView);
		CCDirector.sharedDirector().setDisplayFPS(true);
		CCDirector.sharedDirector().setAnimationInterval(1.0f / 60.0f);

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

		Log.i(getClass().getName(), "onActivityResult");

		super.onActivityResult(request, response, data);
		mHelper.onActivityResult(request, response, data);

		if (request == SceneManager.REQUEST_SELECTPLAYERS && response == RESULT_OK) {

			ArrayList<String> invitees = data.getStringArrayListExtra(GamesClient.EXTRA_PLAYERS);

			// get auto-match criteria
			Bundle autoMatchCriteria = null;
			int minAutoMatchPlayers = data.getIntExtra(GamesClient.EXTRA_MIN_AUTOMATCH_PLAYERS, 0);
			int maxAutoMatchPlayers = data.getIntExtra(GamesClient.EXTRA_MAX_AUTOMATCH_PLAYERS, 0);
			if (minAutoMatchPlayers > 0) {
				autoMatchCriteria = RoomConfig.createAutoMatchCriteria(minAutoMatchPlayers, maxAutoMatchPlayers, 0);
			} else {
				autoMatchCriteria = null;
			}

			TurnBasedMatchConfig tbmc = TurnBasedMatchConfig.builder().addInvitedPlayers(invitees).setAutoMatchCriteria(autoMatchCriteria).build();

			// kick the match off
			mHelper.getGamesClient().createTurnBasedMatch(this, tbmc);

		} else if (request == SceneManager.REQUEST_MATCHINBOX) {

			Log.i(getClass().getName(), "Result from Match inbox");

			if (response == RESULT_OK) {

				TurnBasedMatch match = data.getParcelableExtra(GamesClient.EXTRA_TURN_BASED_MATCH);
				if (match != null) {
					sceneManager.showGoogleTurnbasedMatchGame(match);
				}
			}
		}
	}

	@Override
	public void onSignInFailed() {
		sceneManager.showMainMenu(false);
	}

	@Override
	public void onSignInSucceeded() {
		Log.i(getClass().getName(), "onSignInSucceeded");

		TurnBasedMatch match = mHelper.getTurnBasedMatch();
		if (match != null) {
			Log.i(getClass().getName(), "onSignInSucceeded - Notification match was found - Status=" + match.getStatus());

			sceneManager.showGoogleTurnbasedMatchGame(match);

		} else {
			sceneManager.showMainMenu(true);
		}

		/*
		 * String invitation = mHelper.getInvitationId(); if (invitation !=
		 * null) { Log.i(getClass().getName(),
		 * "onSignInSucceeded - Invitation match was found - Id=" + invitation);
		 * 
		 * }
		 */

	}

	@Override
	public boolean onKeyDown(int keycode, KeyEvent e) {
		switch (keycode) {
		case KeyEvent.KEYCODE_BACK:
			if(sceneManager.backPressed()) {
				return true;
			}
		}
		return super.onKeyDown(keycode, e);
	}

	@Override
	public void onTurnBasedMatchInitiated(int statusCode, TurnBasedMatch match) {

		int status = match.getStatus();
		int turnStatus = match.getTurnStatus();

		Log.i(getClass().getName(), "onTurnBasedMatchInitiated. Status=" + status + ", Turnstatus=" + turnStatus);

		// match.getData();
		//mHelper.getGamesClient().takeTurn(this, match.getMatchId(), null, getNextParticipantId(match));
		
		sceneManager.showGoogleTurnbasedMatchGame(match);
	}

	@Override
	public void onTurnBasedMatchUpdated(int statusCode, TurnBasedMatch match) {

		Log.i(getClass().getName(), "onTurnBasedMatchUpdated");
		// TODO Auto-generated method stub

	}	
}
