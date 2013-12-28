package com.wotr.cocos;

import java.util.ArrayList;
import java.util.Collection;
import java.util.Iterator;

import org.cocos2d.actions.ease.CCEaseSineIn;
import org.cocos2d.actions.instant.CCCallback;
import org.cocos2d.actions.interval.CCDelayTime;
import org.cocos2d.actions.interval.CCFadeIn;
import org.cocos2d.actions.interval.CCFadeOut;
import org.cocos2d.actions.interval.CCMoveTo;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.actions.interval.CCTintTo;
import org.cocos2d.layers.CCLayer;
import org.cocos2d.layers.CCScene;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCLabel;
import org.cocos2d.nodes.CCNode;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.sound.SoundEngine;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;
import org.cocos2d.types.ccColor3B;

import android.content.res.AssetFileDescriptor;
import android.media.MediaPlayer;

import com.google.example.games.basegameutils.GameHelper;
import com.wotr.GameManager;
import com.wotr.R;
import com.wotr.cocos.action.RemoveNodeCallBackAction;
import com.wotr.cocos.nodes.ActionPathSprite;
import com.wotr.cocos.nodes.BonusSelectionActionListener;
import com.wotr.cocos.nodes.BonusSelectionSprite;
import com.wotr.cocos.nodes.CardSprite;
import com.wotr.cocos.nodes.EndPositionSelectionActionListener;
import com.wotr.cocos.nodes.EndPositionSelectionSprite;
import com.wotr.model.Action;
import com.wotr.model.AttackResult;
import com.wotr.model.Position;
import com.wotr.model.attack.AttackEndPosition;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.attribute.bonus.BonusAward;
import com.wotr.strategy.action.ActionCollection;
import com.wotr.strategy.action.ActionsResolver;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.action.PathFinderStrategy;
import com.wotr.strategy.action.ShortestPathFinderStrategy;
import com.wotr.strategy.battle.BattleListener;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.GameEventListener;
import com.wotr.strategy.game.MultiplayerGame;
import com.wotr.strategy.game.exceptions.InvalidActionException;
import com.wotr.strategy.game.exceptions.InvalidAttackException;
import com.wotr.strategy.game.exceptions.InvalidMoveException;
import com.wotr.strategy.player.HumanPlayer;
import com.wotr.strategy.player.Player;
import com.wotr.touch.CardTouchGridDecorator;
import com.wotr.touch.CardTouchListener;

public class PlayGameLayer extends AbstractGameLayer implements CardTouchListener, GameEventListener, BattleListener, EndPositionSelectionActionListener, BonusSelectionActionListener {

	private Collection<CardSprite> unitList = new ArrayList<CardSprite>();
	private int xCount;
	private int yCount;
	private ActionCollection<Action> actionCollection;
	private CCLabel nameLabel;
	private CCLabel turnLabel;
	private Player playerOne;
	private ActionsResolverStrategy actionsResolver;

	private PathFinderStrategy pathFinderStrategy;
	private ActionPathSprite actionPathSprite;

	public static CCScene scene(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap, GameHelper mHelper) {
		CCScene scene = CCScene.node();
		CCLayer layer = new PlayGameLayer(playerOneMap, playerTwoMap, mHelper);
		scene.addChild(layer);
		return scene;
	}

	protected PlayGameLayer(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap, GameHelper mHelper) {

		xCount = 5;
		yCount = 8;

		String playerOneName = "Player 1";

		if (mHelper.isSignedIn()) {
			com.google.android.gms.games.Player p = mHelper.getGamesClient().getCurrentPlayer();

			if (p != null) {
				playerOneName = p.getDisplayName();
			}
		}

		playerOne = new HumanPlayer(playerOneMap, playerOneName, 0);
		Player playerTwo = new HumanPlayer(playerTwoMap, "Player 2", yCount - 1);

		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		CCSprite back = new CCSprite("woddenbackground.png");

		back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		addChild(back);

		CCSprite prototype = new CCSprite("unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;

		addBackGroundCards(xCount, yCount, true);
		addCards(playerOneMap);
		addCards(playerTwoMap);

		nameLabel = CCLabel.makeLabel("    ", "Arial", 50f);
		nameLabel.setPosition(winSize.getWidth() - 30f, winSize.getHeight() - 100f);
		nameLabel.setAnchorPoint(0f, 0.5f);
		nameLabel.setRotation(90f);
		// nameLabel.setOpacity(150);
		addChild(nameLabel, 10);

		turnLabel = CCLabel.makeLabel("    ", "Arial", 60f);
		turnLabel.setPosition(winSize.getWidth() - 30f, winSize.getHeight() - 80f);
		turnLabel.setAnchorPoint(0.5f, 0f);
		// turnLabel.setOpacity(150);
		addChild(turnLabel, 10);

		Game game = new MultiplayerGame(playerOne, playerTwo);
		game.addGameEventListener(this);
		GameManager.setGame(game);
		GameManager.getFactory().getBattleStrategy().addBattleListener(this);

		actionsResolver = new ActionsResolver(xCount, yCount, game);
		game.setActionsResolver(actionsResolver);

		game.startGame();
	}

	protected void dropCardToPosition(CardSprite card) {
		CCScaleTo scaleAction = CCScaleTo.action(0.3f, sizeScale);
		card.runAction(scaleAction);
	}

	private void addCards(UnitMap<Position, Unit> playerCards) {

		CardTouchGridDecorator gridDecorator = new CardTouchGridDecorator(bordframe);
		gridDecorator.addCardTouchListener(this);

		for (Unit card : playerCards.values()) {
			CardSprite cardSpite = new CardSprite(card, sizeScale, bordframe);
			addChild(cardSpite);
			cardSpite.addListener(gridDecorator);
			unitList.add(cardSpite);

			cardSpite.drawBonus();
		}
	}

	@Override
	public boolean cardDragedStarted(CardSprite card) {

		boolean cardTouchStarted = isTurn((Unit) card.getUserData());
		if (cardTouchStarted) {

			/*
			 * if (card.numberOfRunningActions() == 0) { originalPosition =
			 * selectedCard.getPosition(); }
			 */
			reorderChild(card, 1);
			selectCardForMove(card);
		}

		return cardTouchStarted;
	}

	@Override
	public void cardDragedEnded(CardSprite card, float x, float y) {

		resetActionSelection(card);

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			moveCardToOriginalPosition(card);
			removeSelection(card);
		} else {

			Unit attackingUnit = (Unit) card.getUserData();

			// If player already has card at position, move back
			if (GameManager.getGame().getAttackingPlayer().hasUnitAtPosition(pInP)) {
				moveCardToOriginalPosition(card);
				removeSelection(card);
			} else {

				Unit defendingUnit = GameManager.getGame().getDefendingPlayer().getUnitAtPosition(pInP);
				pathFinderStrategy.getActionForPosition(pInP);

				try {
					// if defending unit found on position, perform attack
					if (defendingUnit != null) {
						cardDragedEndedOnDefendingUnit(card, attackingUnit, defendingUnit, pInP);
					} else {
						cardDragedEndedOnEmptyPosition(card, attackingUnit, pInP);
						removeSelection(card);
					}
				} catch (InvalidActionException e) {
					moveCardToOriginalPosition(card);
				}
			}
		}
	}

	private void removeSelection(CardSprite card) {
		reorderChild(card, 1);
	}

	private void cardDragedEndedOnEmptyPosition(CardSprite card, Unit attackingUnit, Position pInP) throws InvalidMoveException {

		dropCardToPosition(card);

		GameManager.getGame().move(attackingUnit, pInP);
		SoundEngine.sharedEngine().playEffect(CCDirector.sharedDirector().getActivity(), R.raw.pageflip);
	}

	private void cardDragedEndedOnDefendingUnit(CardSprite card, Unit attackingUnit, Unit defendingUnit, Position pInP) throws InvalidAttackException {

		Action action = pathFinderStrategy.getActionForPosition(pInP);
		if (action != null) {

			AttackResult attackResult = GameManager.getGame().attack(action, defendingUnit);

			if (attackResult.isSuccesfull()) {
				removeCCSprite(defendingUnit);
			}

			// If there is only one possible endposition after attack,
			// automatically use it, otherwise ask the user
			Collection<AttackEndPosition> endPositions = attackResult.getEndPositionProspects();
			if (endPositions.size() == 1) {
				AttackEndPosition endPosition = attackResult.getAttackEndPosition();
				endPosition.endAttack();
				moveCardToPosition(card, endPosition.getPosition());
				removeSelection(card);
				awardBonus(attackResult);
			} else {

				dropCardToPosition(card);

				// Add images to endposition selection positions for units
				for (AttackEndPosition endPosition : endPositions) {
					EndPositionSelectionSprite goSprite = new EndPositionSelectionSprite(card, endPosition, sizeScale, bordframe);
					goSprite.addActionListener(this);
					addChild(goSprite, 10);
				}
			}
		} else {
			moveCardToOriginalPosition(card);
		}
	}

	private void awardBonus(AttackResult attackResult) {

		Collection<BonusAward> awardProspects = attackResult.getAwardProspects();
		if (!awardProspects.isEmpty()) {

			BonusSelectionSprite bss = new BonusSelectionSprite(awardProspects);
			bss.setPosition(CGPoint.ccp(winSize.getWidth() / 2f, winSize.getHeight() / 2f));
			bss.addActionListener(this);
			addChild(bss, 100);
		} else {
			// Attack has ended
		}
	}

	@Override
	public void bonusSelected(BonusAward award) {
		award.claim();
	}

	private void resetActionSelection(CardSprite card) {

		removePathSprite();

		Collection<Position> attackPositions = actionCollection.getAttackPositions();
		for (Position position : attackPositions) {
			for (CCNode ccNode : unitList) {

				Unit unit = (Unit) ccNode.getUserData();
				if (position.equals(unit.getPosition())) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccWHITE);
					ccNode.runAction(tin);
				}
			}
		}

		Collection<Position> movePositions = actionCollection.getMovePositions();
		for (Position position : movePositions) {
			for (CCNode ccNode : cardBackgroundList) {
				Position pos = (Position) ccNode.getUserData();
				if (position.equals(pos)) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccWHITE);
					ccNode.runAction(tin);
				}
			}
		}

		card.setOpacity(255);
	}

	protected void selectCardForMove(CCSprite selectedCard) {
		super.selectCardForMove(selectedCard);

		Unit unit = (Unit) selectedCard.getUserData();

		actionCollection = actionsResolver.getActions(unit);
		pathFinderStrategy = new ShortestPathFinderStrategy(actionCollection);

		for (Position position : actionCollection.getAttackPositions()) {
			for (CCNode ccNode : unitList) {
				Unit u = (Unit) ccNode.getUserData();
				if (position.equals(u.getPosition())) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccRED);
					ccNode.runAction(tin);
				}
			}
		}

		for (Position position : actionCollection.getMovePositions()) {
			for (CCNode ccNode : cardBackgroundList) {
				Position pos = (Position) ccNode.getUserData();
				if (position.equals(pos)) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccGREEN);
					ccNode.runAction(tin);
				}
			}
		}
	}

	@Override
	public void cardMoved(CardSprite card, float x, float y, boolean originalPosition) {
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			card.setPosition(x, y);
		} else {
			CGPoint position = bordframe.getPosition(pInP.getX(), pInP.getY());

			if (!CGPoint.equalToPoint(card.getPosition(), position)) {
				card.setPosition(position);
				pathFinderStrategy.touch(pInP);
				Action action = pathFinderStrategy.getActionForPosition(pInP);

				removePathSprite();

				if (action != null) {
					actionPathSprite = new ActionPathSprite(action, bordframe);
					addChild(actionPathSprite);
				}
			}
		}
	}

	private void removePathSprite() {
		if (actionPathSprite != null) {
			removeChild(actionPathSprite, true);
		}
	}

	@Override
	public void cardSelected(CardSprite card, float x, float y) {
		moveCardToCenterAndEnlarge(card);
	}

	@Override
	public void cardDeSelected(CardSprite card, float x, float y) {
		resetActionSelection(card);
		moveCardToOriginalPosition(card);
	}

	@Override
	public void gameStarted() {
	}

	@Override
	public void startTurn(Player player, int actionsLeft) {
		turnLabel.setString("" + actionsLeft);
		nameLabel.setString(player.getName());

		if (player.equals(playerOne)) {
			turnLabel.setColor(ccColor3B.ccGREEN);
			nameLabel.setColor(ccColor3B.ccGREEN);
		} else {
			turnLabel.setColor(ccColor3B.ccRED);
			nameLabel.setColor(ccColor3B.ccRED);
		}
	}

	@Override
	public void actionPerformed(Player player, int remainingActions) {
		startTurn(player, remainingActions);
	}

	@Override
	protected boolean isTurn(Unit unit) {
		return GameManager.getGame().getAttackingPlayer().hasUnit(unit);
	}

	private void removeCCSprite(Unit defendingUnit) {

		for (Iterator<CardSprite> i = unitList.iterator(); i.hasNext();) {
			CCSprite unitSpite = i.next();
			Unit unit = (Unit) unitSpite.getUserData();
			if (unit.equals(defendingUnit)) {
				i.remove();
				removeChild(unitSpite, true);
				return;
			}
		}
	}

	@Override
	public void attackStarted(Unit attacker, Unit defender) {

		MediaPlayer mp = new MediaPlayer();
		try {
			AssetFileDescriptor afd = CCDirector.sharedDirector().getActivity().getAssets().openFd(attacker.getAttackSound());
			mp.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
			mp.prepare();
			mp.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void attackSuccessful(Unit attacker, Unit defender, int attackRoll) {

		CCLabel actionLabel = CCLabel.makeLabel("Attack succesful (" + attackRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);

		addChild(actionLabel);

		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(moveAction, fadeAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));

	}

	@Override
	public void attackFailed(Unit attacker, Unit defender, int attackRoll) {

		// CCNode node = CCNode.node();
		// node.setPosition(winSize.width / 2, winSize.height - winSize.height /
		// 3f);

		// CCSprite dice = CCSprite.sprite("dice/1.png");
		// dice.setPosition(100f, 10f);
		// node.addChild(dice);

		CCLabel actionLabel = CCLabel.makeLabel("Missed (" + attackRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		// node.addChild(actionLabel);

		addChild(actionLabel, 100);

		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(moveAction, fadeAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));
	}

	@Override
	public void defenceStarted(Unit attacker, Unit defender) {

	}

	@Override
	public void defenceSuccessful(Unit attacker, Unit defender, int defenceRoll) {
		CCLabel actionLabel = CCLabel.makeLabel("Defence succesful (" + defenceRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		actionLabel.setOpacity(0);

		addChild(actionLabel, 100);

		CCDelayTime delayAction = CCDelayTime.action(0.1f);
		CCFadeIn fadeInAction = CCFadeIn.action(0.3f);
		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(delayAction, fadeInAction, moveAction, fadeAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));
	}

	@Override
	public void defenceFailed(Unit attacker, Unit defender, int defenceRoll) {

		MediaPlayer mp = new MediaPlayer();
		try {
			AssetFileDescriptor afd = CCDirector.sharedDirector().getActivity().getAssets().openFd(defender.getKilledSound());
			mp.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
			mp.prepare();
			mp.start();
		} catch (Exception e) {
			e.printStackTrace();
		}

		CCLabel actionLabel = CCLabel.makeLabel("Defence failed (" + defenceRoll + ")", "Arial", 40f);
		actionLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		actionLabel.setOpacity(0);

		addChild(actionLabel, 100);

		CCDelayTime delayAction = CCDelayTime.action(0.1f);
		CCFadeIn fadeInAction = CCFadeIn.action(0.3f);
		CCMoveTo moveAction = CCMoveTo.action(2.0f, CGPoint.ccp(winSize.width / 2, winSize.height + 50));
		CCFadeOut fadeOutAction = CCFadeOut.action(3.0f);
		CCCallback cleanupAction = CCCallback.action(new RemoveNodeCallBackAction(this, actionLabel));

		CCSequence seq = CCSequence.actions(delayAction, fadeInAction, moveAction, fadeOutAction, cleanupAction);
		actionLabel.runAction(CCEaseSineIn.action(seq));
	}

	@Override
	public void gameEnded(Player winner) {

		CCLabel winnerLabel = CCLabel.makeLabel("Winner: " + winner.getName(), "Arial", 40f);
		winnerLabel.setPosition(winSize.width / 2, winSize.height - winSize.height / 3f);
		addChild(winnerLabel);

		MediaPlayer mp = new MediaPlayer();
		try {
			AssetFileDescriptor afd = CCDirector.sharedDirector().getActivity().getAssets().openFd("sounds/fanfare.mp3");
			mp.setDataSource(afd.getFileDescriptor(), afd.getStartOffset(), afd.getLength());
			mp.prepare();
			mp.start();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void endPositionSelected(EndPositionSelectionSprite goSprite, CardSprite card, AttackEndPosition endPosition) {
		Position position = endPosition.getPosition();
		endPosition.endAttack();
		moveCardToPosition(card, position);
		awardBonus(endPosition.getAttackResult());
	}
}
