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
	private TurnStrategy turnStrategy;

	public MultiplayerGame(Player playerOne, Player playerTwo) {
		this.playerOne = playerOne;
		this.playerTwo = playerTwo;
	}

	@Override
	public void startGame() {

		turnStrategy = GameManager.getFactory().getTurnStrategy();
		turnStrategy.resetGame();
		listener.gameStarted();

		Random random = new Random();
		currentPlayer = random.nextBoolean() ? playerOne : playerTwo;

		listener.startTurn(currentPlayer, turnStrategy.getRemainingActions());
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
		turnStrategy.attack(attackingUnit);
		BattleStrategy bs = GameManager.getFactory().getBattleStrategy();
		boolean succes = bs.battle(attackingUnit, defendingUnit);
		if (succes) {
			Position defendingPosition = defendingUnit.getPosistion();
			getDefendingPlayer().getUnitMap().remove(defendingPosition);

			if (!attackingUnit.isRanged()) {
				getAttackingPlayer().getUnitMap().remove(attackingUnit.getPosistion());
				getAttackingPlayer().getUnitMap().put(defendingPosition, attackingUnit);
			}
		}
		notifyGameActionListener();
		return succes;
	}

	@Override
	public void move(Position oldPosition, Position newPosition) {
		Unit movedUnit = getAttackingPlayer().getUnitMap().remove(oldPosition);
		if (movedUnit != null) {
			getAttackingPlayer().getUnitMap().put(newPosition, movedUnit);
		}

		turnStrategy.move(movedUnit);
		notifyGameActionListener();
	}

	private void notifyGameActionListener() {
		if (turnStrategy.getRemainingActions() == 0) {
			currentPlayer = getDefendingPlayer();
			listener.startTurn(currentPlayer, turnStrategy.resetTurn());
		} else {
			listener.actionPerformed(currentPlayer, turnStrategy.getRemainingActions());
		}
	}
}
