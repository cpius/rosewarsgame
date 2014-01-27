package com.wotr;

import com.google.android.gms.games.multiplayer.turnbased.TurnBasedMatch;
import com.wotr.strategy.game.Game;

public interface SceneManager {

	public static final int REQUEST_ACHIEVEMENTS = 0;
	public static final int REQUEST_LEADERBOARD = 1;
	public static final int REQUEST_SELECTPLAYERS = 2;
	public static final int REQUEST_MATCHINBOX = 3;

	public void showMainMenu(boolean signedIn);

	public void showGoogleTurnbasedMatchGame(TurnBasedMatch match);

	public void showMatch(Game game);

	public boolean backPressed();

}
