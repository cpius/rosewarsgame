package com.wotr.cocos;

import java.util.Collection;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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

import com.wotr.GameManager;
import com.wotr.R;
import com.wotr.model.Action;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.GameEventListener;
import com.wotr.strategy.game.MultiplayerGame;
import com.wotr.strategy.impl.ActionResolver;
import com.wotr.strategy.player.HumanPlayer;
import com.wotr.strategy.player.Player;
import com.wotr.touch.CardTouchHandler;
import com.wotr.touch.CardTouchListener;

public class PlayGameLayer extends AbstractGameLayer implements CardTouchListener, GameEventListener {

	private Map<CCSprite, Unit> modelMap = new HashMap<CCSprite, Unit>();
	private int xCount;
	private int yCount;
	//private final UnitMap<Position, Unit> playerOneMap;
	//private final UnitMap<Position, Unit> playerTwoMap;
	private Collection<Action> actions;
	private CCLabel nameLabel;
	private CCLabel turnLabel;
	private HumanPlayer playerOne;

	public static CCScene scene(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap) {
		CCScene scene = CCScene.node();
		CCLayer layer = new PlayGameLayer(playerOneMap, playerTwoMap);
		scene.addChild(layer);
		return scene;
	}

	protected PlayGameLayer(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap) {

		playerOne = new HumanPlayer(playerOneMap, "Player 1");
		Player playerTwo = new HumanPlayer(playerTwoMap, "Player 2");

		// this.cards = cards;
		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		xCount = 5;
		yCount = 8;

		CCSprite back = CCSprite.sprite("woddenbackground.png");

		back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		addChild(back);

		CCSprite prototype = CCSprite.sprite("unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		tch = new CardTouchHandler();
		tch.addListener(this);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;

		addBackGroundCards(xCount, yCount, true);
		addCards(playerOneMap);
		addCards(playerTwoMap);

		nameLabel = CCLabel.makeLabel("    ", "Arial", 60f);
		nameLabel.setPosition(10f, winSize.getHeight() - 80f);
		nameLabel.setAnchorPoint(0, 0);
		nameLabel.setColor(ccColor3B.ccWHITE);
		nameLabel.setOpacity(200);
		addChild(nameLabel, 10);

		turnLabel = CCLabel.makeLabel("    ", "Arial", 60f);
		turnLabel.setPosition(winSize.getWidth() - 50f, winSize.getHeight() - 80f);
		turnLabel.setAnchorPoint(0, 0);
		turnLabel.setColor(ccColor3B.ccWHITE);
		turnLabel.setOpacity(200);
		addChild(turnLabel, 10);

		Game game = new MultiplayerGame(playerOne, playerTwo);
		game.addGameEventListener(this);
		GameManager.setGame(game);
		game.startGame();
	}

	protected void moveCardToPosition() {
		SoundEngine.sharedEngine().playEffect(CCDirector.sharedDirector().getActivity(), R.raw.pageflip);
		CCScaleTo scaleAction = CCScaleTo.action(0.3f, sizeScale);
		CCSequence seq = CCSequence.actions(scaleAction);
		selectedCard.runAction(seq);
	}

	private void addCards(UnitMap<Position, Unit> playerCards) {

		for (Unit card : playerCards.values()) {
			Position pos = card.getPosistion();
			CGPoint point = bordframe.getPosition(pos.getX(), pos.getY());
			CCSprite cardSprite = CCSprite.sprite(card.getImage());
			cardSprite.setPosition(point);
			cardSprite.setScale(sizeScale);
			cardSprite.setUserData(pos);
			addChild(cardSprite);

			modelMap.put(cardSprite, card);
		}
	}

	@Override
	public void cardDragedEnded(float x, float y) {

		resetActionSelection();

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			moveCardToOriginalPosition();
		} else {
			moveCardToPosition();
			
			GameManager.getGame().move((Position)selectedCard.getUserData(), pInP);

			selectedCard.setUserData(pInP);
		}

		reorderChild(selectedCard, 0);
		selectedCard = null;
	}

	private void resetActionSelection() {
		List<CCNode> children = getChildren();
		for (Action action : actions) {
			for (CCNode ccNode : children) {
				boolean contains = action.getPosition().equals(ccNode.getUserData());
				if (contains) {
					CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccWHITE);
					ccNode.runAction(tin);
				}
			}
		}
	}

	protected void selectCardForMove(CCSprite selectedCard) {
		super.selectCardForMove(selectedCard);

		Unit unit = modelMap.get(selectedCard);

		ActionResolver ar = new ActionResolver(xCount, yCount);

		Game game = GameManager.getGame();
		
		actions = ar.getActions(unit, game.getAttackingPlayer().getUnitMap(), game.getDefendingPlayer().getUnitMap());
		
		List<CCNode> children = getChildren();
		for (Action action : actions) {
			for (CCNode ccNode : children) {
				boolean contains = action.getPosition().equals(ccNode.getUserData());
				if (contains) {
					markeNodeForAction(action, ccNode);
				}
			}
		}
	}

	private void markeNodeForAction(Action action, CCNode ccNode) {
		if (action instanceof MoveAction) {
			CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccGREEN);
			ccNode.runAction(tin);
		} else {
			CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccRED);
			ccNode.runAction(tin);
		}
	}

	@Override
	public void cardMoved(float x, float y) {
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			selectedCard.setPosition(x, y);
		} else {
			CGPoint position = bordframe.getPosition(pInP.getX(), pInP.getY());
			selectedCard.setPosition(position);
		}
	}

	@Override
	public void cardSelected(float x, float y) {
		moveCardToCenterAndEnlarge();
	}

	@Override
	public void cardDeSelected(float x, float y) {
		moveCardToOriginalPosition();

		resetActionSelection();
	}

	@Override
	protected Collection<CCSprite> getCardSprites() {
		return modelMap.keySet();
	}

	@Override
	public void gameStarted() {
		// TODO Auto-generated method stub

	}

	@Override
	public void startTurn(Player player, int actionsLeft) {
		turnLabel.setString("" + actionsLeft);
		nameLabel.setString(player.getName());
		
		if(player.equals(playerOne)) {
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
	protected boolean isTurn(Position pos) {
		return GameManager.getGame().getAttackingPlayer().getUnitMap().containsKey(pos);
	}

}
