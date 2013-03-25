package com.wotr.strategy.game;

import java.util.Random;

import com.wotr.GameManager;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.player.Player;

/**
 * A multiplayer game is a game where two human players are playing against each
 * other on the seame device.
 * 
 * @author hansenp
 * 
 */
public class MultiplayerGame implements Game {

	private final Player playerOne;
	private final Player playerTwo;

	private Player currentPlayer;
	private GameEventListener listener;
	private TurnStrategy ts;

	public MultiplayerGame(Player playerOne, Player playerTwo) {
		this.playerOne = playerOne;
		this.playerTwo = playerTwo;
	}

	@Override
	public void startGame() {

		ts = GameManager.getFactory().getTurnStrategy();
		ts.resetGame();
		listener.gameStarted();

		Random random = new Random();
		currentPlayer = random.nextBoolean() ? playerOne : playerTwo;

		listener.startTurn(currentPlayer, ts.getRemainingActions());
	}

	@Override
	public Player getAttackingPlayer() {
		return currentPlayer;
	}

	@Override
	public Player getDefendingPlayer() {
		return currentPlayer.equals(playerOne) ? playerTwo : playerOne;
	}

	@Override
	public void addGameEventListener(GameEventListener listener) {
		this.listener = listener;
	}

	@Override
	public boolean attack(Unit attackingUnit, Unit defendingUnit) {
		ts.attack(attackingUnit);
		BattleStrategy bs = GameManager.getFactory().getBattleStrategy();
		boolean result = bs.battle(attackingUnit, defendingUnit);
		doAction();
		return result;
	}

	@Override
	public void move(Position oldPosition, Position newPosition) {

		Unit movedUnit = currentPlayer.getUnitMap().remove(oldPosition);
		if (movedUnit != null) {
			currentPlayer.getUnitMap().put(newPosition, movedUnit);
		}

		ts.move(movedUnit);
		doAction();
	}

	private void doAction() {
		if (ts.getRemainingActions() == 0) {
			currentPlayer = getDefendingPlayer();
			listener.startTurn(currentPlayer, ts.resetTurn());
		} else {
			listener.actionPerformed(currentPlayer, ts.getRemainingActions());
		}
	}
}
