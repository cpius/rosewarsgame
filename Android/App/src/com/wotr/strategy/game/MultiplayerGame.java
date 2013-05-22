package com.wotr.strategy.game;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Random;

import com.wotr.GameManager;
import com.wotr.model.Action;
import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.attack.FailedMeleeAttackEndpoint;
import com.wotr.model.attack.FailedRangedAttackEndpoint;
import com.wotr.model.attack.SuccessfulMeleeAttackEndpoint;
import com.wotr.model.attack.SuccessfulRangedAttackEndpoint;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.attribute.bonus.AttackBonusAward;
import com.wotr.model.unit.attribute.bonus.BonusAward;
import com.wotr.model.unit.attribute.bonus.DefenceBonusAward;
import com.wotr.strategy.action.ActionCollection;
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
public class MultiplayerGame implements Game, AttackEnder {

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
	public AttackResult attack(Action action, Unit defendingUnit) throws InvalidAttackException {
		Unit attackingUnit = action.getUnit();
		validateAttack(attackingUnit, defendingUnit);

		turnStrategy.attack(attackingUnit);
		BattleStrategy bs = GameManager.getFactory().getBattleStrategy();
		boolean succes = bs.battle(attackingUnit, defendingUnit);

		Position defendingPosition = defendingUnit.getPosition();

		Collection<BonusAward> awardProspects = new ArrayList<BonusAward>();

		if (succes) {

			// Rewrite this
			awardProspects.addAll(getAwardProspects(attackingUnit));

			// Remove defeated unit from defending player
			getDefendingPlayer().getUnitMap().remove(defendingPosition);

			if (attackingUnit.isRanged()) {
				// If successful attacking unit is ranged, keep position
				AttackResult result = new AttackResult(succes, awardProspects);
				result.addEndposition(new SuccessfulRangedAttackEndpoint(this, attackingUnit, attackingUnit.getPosition()));
				return result;
			} else {
				// If successful attacking unit is melee, suggest end positions
				AttackResult result = new AttackResult(succes, awardProspects);
				result.addEndposition(new SuccessfulMeleeAttackEndpoint(this, attackingUnit, action.getPath().getPosition()));
				result.addEndposition(new SuccessfulMeleeAttackEndpoint(this, attackingUnit, attackingUnit.getPosition()));
				return result;
			}
		} else {
			if (attackingUnit.isRanged()) {
				// If failed attacking unit is ranged, keep position
				AttackResult result = new AttackResult(succes, awardProspects);
				result.addEndposition(new FailedRangedAttackEndpoint(this, attackingUnit, attackingUnit.getPosition()));
				return result;
			} else {
				// If failed attacking unit is melee, go back to attacking
				// position
				Position position = null;
				if (action.getPath().getPreviousPath() != null) {
					position = action.getPath().getPreviousPath().getPosition();
				} else {
					position = action.getUnit().getPosition();
				}

				AttackResult result = new AttackResult(succes, awardProspects);
				result.addEndposition(new FailedMeleeAttackEndpoint(this, attackingUnit, position));
				return result;
			}
		}
	}

	// Move this shit to a better location
	private Collection<? extends BonusAward> getAwardProspects(Unit attackingUnit) {

		Collection<BonusAward> result = new ArrayList<BonusAward>();
		
		int xp = attackingUnit.addExperience();

		// if award is to be given
		if (xp >= 2) {
			attackingUnit.resetExperience();
			result.add(new AttackBonusAward(attackingUnit));
			result.add(new DefenceBonusAward(attackingUnit));
		} 

		return result;
	}

	@Override
	public void endAttack(Unit attackingUnit, Position endPosition, boolean moved) {
		if (moved) {
			getAttackingPlayer().getUnitMap().remove(attackingUnit.getPosition());
			getAttackingPlayer().getUnitMap().put(endPosition, attackingUnit);
		}
		notifyGameActionListener();
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

	public void notifyGameActionListener() {

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
		ActionCollection<Action> actionCollection = actionsResolver.getActions(attackingUnit);
		Collection<Action> actions = actionCollection.getActions();
		for (Action action : actions) {
			if (action.getPosition().equals(defendingUnit.getPosition())) {
				return;
			}
		}

		throw new InvalidAttackException(attackingUnit, defendingUnit);
	}

	private void validateMove(Unit movingUnit, Position newPosition) throws InvalidMoveException {
		ActionCollection<Action> actionCollection = actionsResolver.getActions(movingUnit);
		Collection<Action> actions = actionCollection.getActions();
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
