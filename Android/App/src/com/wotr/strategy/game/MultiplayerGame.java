package com.wotr.strategy.game;

import java.util.Collection;
import java.util.Random;

import com.wotr.GameManager;
import com.wotr.model.Action;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.game.exceptions.InvalidAttackException;
import com.wotr.strategy.game.exceptions.InvalidMoveException;
import com.wotr.strategy.player.Player;

/**
 * A multiplayer game is a game where two human players are playing against each
 * other on the same device.
 * 
 * @author hansenp
 * 
 */
public class MultiplayerGame implements Game {

	private final Player playerOne;
	private final Player playerTwo;

	private Player currentPlayer;
	private TurnStrategy turnStrategy;
	private GameEventListenerCollection listeners = new GameEventListenerCollection();
	private ActionsResolverStrategy actionsResolver;

	public MultiplayerGame(Player playerOne, Player playerTwo) {
		this.playerOne = playerOne;
		this.playerTwo = playerTwo;
	}

	@Override
	public void startGame() {

		turnStrategy = GameManager.getFactory().getTurnStrategy();
		turnStrategy.resetGame();
		listeners.gameStarted();

		Random random = new Random();
		currentPlayer = random.nextBoolean() ? playerOne : playerTwo;

		listeners.startTurn(currentPlayer, turnStrategy.getRemainingActions());
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
		listeners.add(listener);
	}

	@Override
	public boolean attack(Unit attackingUnit, Unit defendingUnit) throws InvalidAttackException {
		validateAttack(attackingUnit, defendingUnit);

		turnStrategy.attack(attackingUnit);
		BattleStrategy bs = GameManager.getFactory().getBattleStrategy();
		boolean succes = bs.battle(attackingUnit, defendingUnit);
		if (succes) {
			Position defendingPosition = defendingUnit.getPosition();
			getDefendingPlayer().getUnitMap().remove(defendingPosition);

			if (!attackingUnit.isRanged()) {
				getAttackingPlayer().getUnitMap().remove(attackingUnit.getPosition());
				getAttackingPlayer().getUnitMap().put(defendingPosition, attackingUnit);
			}
		}
		notifyGameActionListener();
		return succes;
	}

	@Override
	public void move(Unit movingUnit, Position newPosition) throws InvalidMoveException {
		validateMove(movingUnit, newPosition);

		Unit movedUnit = getAttackingPlayer().getUnitMap().remove(movingUnit.getPosition());
		if (movedUnit != null) {
			getAttackingPlayer().getUnitMap().put(newPosition, movedUnit);
		}

		turnStrategy.move(movedUnit);
		notifyGameActionListener();
	}

	private void notifyGameActionListener() {

		if (victorious()) {
			listeners.gameEnded(currentPlayer);
		} else if (turnStrategy.getRemainingActions() == 0) {
			currentPlayer = getDefendingPlayer();
			listeners.startTurn(currentPlayer, turnStrategy.resetTurn());
		} else {
			listeners.actionPerformed(currentPlayer, turnStrategy.getRemainingActions());
		}
	}

	private void validateAttack(Unit attackingUnit, Unit defendingUnit) throws InvalidAttackException {
		Collection<Action> actions = actionsResolver.getActions(attackingUnit);
		for (Action action : actions) {
			if (action.getPosition().equals(defendingUnit.getPosition())) {
				return;
			}
		}

		throw new InvalidAttackException(attackingUnit, defendingUnit);
	}

	private void validateMove(Unit movingUnit, Position newPosition) throws InvalidMoveException {
		Collection<Action> actions = actionsResolver.getActions(movingUnit);
		for (Action action : actions) {
			if (action.getPosition().equals(newPosition)) {
				return;
			}
		}

		throw new InvalidMoveException(movingUnit, newPosition);
	}

	@Override
	public void setActionsResolver(ActionsResolverStrategy actionsResolver) {
		this.actionsResolver = actionsResolver;
	}

	private boolean victorious() {
		if (getDefendingPlayer().getUnitMap().size() == 0) {
			return true;
		}

		int startLine = getDefendingPlayer().getStartLine();
		for (Position pos : getAttackingPlayer().getUnitMap().keySet()) {
			if (pos.getY() == startLine) {
				return true;
			}
		}

		return false;
	}
}
