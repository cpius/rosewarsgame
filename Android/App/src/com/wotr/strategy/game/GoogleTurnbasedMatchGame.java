package com.wotr.strategy.game;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import android.util.Log;

import com.google.android.gms.games.multiplayer.Participant;
import com.google.android.gms.games.multiplayer.ParticipantResult;
import com.google.android.gms.games.multiplayer.turnbased.OnTurnBasedMatchUpdatedListener;
import com.google.android.gms.games.multiplayer.turnbased.TurnBasedMatch;
import com.google.example.games.basegameutils.GameHelper;
import com.wotr.model.Position;
import com.wotr.model.persist.GameStateSerializer;
import com.wotr.model.persist.gpgs.GoogleTurnbasedMatchGameState;
import com.wotr.model.persist.gpgs.GoogleTurnbasedMatchGameStateSerializer;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.attribute.RawBonus;
import com.wotr.strategy.DeckDrawStrategy;
import com.wotr.strategy.DeckLayoutStrategy;
import com.wotr.strategy.impl.FixedDeckDrawStrategy;
import com.wotr.strategy.impl.RandomDeckLayoutStrategy;
import com.wotr.strategy.player.HumanPlayer;
import com.wotr.strategy.player.OnlinePlayer;
import com.wotr.strategy.player.Player;

public class GoogleTurnbasedMatchGame extends AbstractGame implements Game, AttackEnder, OnTurnBasedMatchUpdatedListener, GameEventListener {

	private TurnBasedMatch match;

	private GameStateSerializer<GoogleTurnbasedMatchGameState, byte[]> serializer = new GoogleTurnbasedMatchGameStateSerializer();
	GoogleTurnbasedMatchGameState state = null;

	private boolean isSetup;
	private GameHelper mHelper;

	private Map<Player, String> playerMap = new HashMap<Player, String>();

	public GoogleTurnbasedMatchGame(GameHelper mHelper, TurnBasedMatch match) {
		this.mHelper = mHelper;
		this.match = match;

		String currentParticipantId = match.getParticipantId(mHelper.getGamesClient().getCurrentPlayerId());

		// If data is null, initialize game state
		if (match.getData() == null) {

			state = createGameState(match);

			// Game is initializes. Save game state to current Participant
			byte[] stateArray = serializer.serialize(state);
			mHelper.getGamesClient().takeTurn(this, match.getMatchId(), stateArray, currentParticipantId);

		} else {
			// Game state has already been created
			state = serializer.deserialize(match.getData());
			isSetup = state.isSetup(currentParticipantId);

			// If player two in players has no units map
			if (!currentParticipantId.equals(match.getCreatorId()) && state.getPlayerTwoUnits() == null) {
				state.setPlayerTwoUnits(drawDeck());
				byte[] stateArray = serializer.serialize(state);
				mHelper.getGamesClient().takeTurn(this, match.getMatchId(), stateArray, currentParticipantId);
			}
		}

		// Create players
		ArrayList<Participant> participants = match.getParticipants();
		for (Participant participant : participants) {
			String name = participant.getDisplayName();
			String pId = participant.getParticipantId();
			if (participant.getParticipantId().equals(state.getPlayerOneId())) {
				playerOne = createPlayer(pId, currentParticipantId, state.getPlayerOneUnits(), name, 0);
				playerMap.put(playerOne, pId);
			} else {
				playerTwo = createPlayer(pId, currentParticipantId, state.getPlayerTwoUnits(), name, getYTileCount() * 2 - 1);
				playerMap.put(playerTwo, pId);
			}
		}

		currentPlayer = getCurrentPlayer(match, currentParticipantId);

		addGameEventListener(this);
	}

	private Player createPlayer(String participantId, String currentParticipantId, UnitMap<Position, Unit> units, String name, int i) {
		return participantId.equals(currentParticipantId) ? new HumanPlayer(units, name, i) : new OnlinePlayer(units, name, i);
	}

	private GoogleTurnbasedMatchGameState createGameState(TurnBasedMatch match) {
		GoogleTurnbasedMatchGameState state = new GoogleTurnbasedMatchGameState();

		// Draw deck for the current player. This will the inviting player
		UnitMap<Position, Unit> deck = drawDeck();
		state.setPlayerOneUnits(deck);

		// Set participantIds in state
		List<String> participantIds = match.getParticipantIds();
		for (String participantId : participantIds) {
			if (participantId.equals(match.getCreatorId())) {
				state.setPlayerOneId(participantId);
			} else {
				state.setPlayerTwoId(participantId);
			}
		}

		return state;
	}

	private UnitMap<Position, Unit> drawDeck() {
		DeckDrawStrategy deckStrategy = new FixedDeckDrawStrategy();
		List<Unit> deck = deckStrategy.drawDeck();

		deck.get(0).getAttackAttribute().addBonus(new RawBonus(1));
		deck.get(1).getDefenceAttribute().addBonus(new RawBonus(1));

		DeckLayoutStrategy layoutStrategy = new RandomDeckLayoutStrategy(getXTileCount(), getYTileCount());
		UnitMap<Position, Unit> layoutDeck = layoutStrategy.layoutDeck(deck);
		return layoutDeck;
	}

	@Override
	public boolean isSetup() {
		return isSetup;
	}

	@Override
	public void setupDone(Player player) {
		isSetup = true;

		// If player one has setup game. Send turn to player two for setup
		if (player.equals(playerOne)) {
			state.setPlayerOneSetup(true);

			String nextPlayer = getNextParticipantId(match);
			currentPlayer = getCurrentPlayer(match, nextPlayer);
			byte[] stateArray = serializer.serialize(state);
			mHelper.getGamesClient().takeTurn(this, match.getMatchId(), stateArray, nextPlayer);
		} else if (player.equals(playerTwo)) {

			// Setup is done in same end of board as player one. Mirror the unit
			// positions
			state.getPlayerTwoUnits().mirrorUnits(getXTileCount(), getYTileCount() * 2);
			state.setPlayerTwoSetup(true);

			// The first user has only one move
			state.setRemainingActions(1);

			// Player two has setup game. Decide who is going to take first
			// turn.
			Random random = new Random();
			String startingPlayerId = random.nextBoolean() ? state.getPlayerOneId() : state.getPlayerTwoId();
			currentPlayer = getCurrentPlayer(match, startingPlayerId);
			byte[] stateArray = serializer.serialize(state);
			mHelper.getGamesClient().takeTurn(this, match.getMatchId(), stateArray, startingPlayerId);
		}
	}

	@Override
	public void onTurnBasedMatchUpdated(int statusCode, TurnBasedMatch match) {
		Log.d(getClass().getName(), "onTurnBasedMatchUpdated. Status = " + statusCode);
	}

	private Player getCurrentPlayer(TurnBasedMatch match, String currentParticipantId) {
		if (match.getTurnStatus() == TurnBasedMatch.MATCH_TURN_STATUS_MY_TURN) {
			return match.getCreatorId().equals(currentParticipantId) ? playerOne : playerTwo;
		} else if (match.getTurnStatus() == TurnBasedMatch.MATCH_TURN_STATUS_THEIR_TURN) {
			return match.getCreatorId().equals(currentParticipantId) ? playerTwo : playerOne;
		} else if (match.getTurnStatus() == TurnBasedMatch.MATCH_TURN_STATUS_COMPLETE) {

		}

		return playerOne;
	}

	public String getNextParticipantId(TurnBasedMatch match) {

		String myParticipantId = match.getParticipantId(mHelper.getGamesClient().getCurrentPlayerId());
		ArrayList<String> participantIds = match.getParticipantIds();

		for (String participantId : participantIds) {
			if (!myParticipantId.equals(participantId)) {
				return participantId;
			}
		}
		throw new IllegalStateException();
	}

	@Override
	public void gameStarted() {

	}

	@Override
	public void gameEnded(Player winner, Player looser) {

		String winnerId = playerMap.get(winner);
		String looserId = playerMap.get(looser);

		byte[] stateArray = serializer.serialize(state);
		ParticipantResult winnerResult = new ParticipantResult(winnerId, ParticipantResult.MATCH_RESULT_WIN, ParticipantResult.PLACING_UNINITIALIZED);
		ParticipantResult looserResult = new ParticipantResult(looserId, ParticipantResult.MATCH_RESULT_LOSS, ParticipantResult.PLACING_UNINITIALIZED);
		mHelper.getGamesClient().finishTurnBasedMatch(this, match.getMatchId(), stateArray, winnerResult, looserResult);

	}

	@Override
	public void startTurn(Player player, int remainingActions) {

	}

	@Override
	public void actionPerformed(Player player, int remainingActions) {

		// Action has been performed by user but turn has not yet ended. Persist
		// the action
		state.setRemainingActions(remainingActions);
		byte[] stateArray = serializer.serialize(state);
		mHelper.getGamesClient().takeTurn(this, match.getMatchId(), stateArray, playerMap.get(player));
	}

	@Override
	public void endTurn(Player player) {

		// At end of turn two new actions i assigned to the next player
		state.setRemainingActions(2);

		byte[] stateArray = serializer.serialize(state);
		mHelper.getGamesClient().takeTurn(this, match.getMatchId(), stateArray, getNextParticipantId(match));
	}

	@Override
	public int getRemainingActions() {
		return state.getRemainingActions();
	}

}
