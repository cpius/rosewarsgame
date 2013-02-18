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
import org.cocos2d.nodes.CCNode;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.sound.SoundEngine;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;
import org.cocos2d.types.ccColor3B;

import com.wotr.R;
import com.wotr.model.Action;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.impl.ActionResolver;
import com.wotr.touch.CardTouchHandler;
import com.wotr.touch.CardTouchListener;

public class PlayGameLayer extends AbstractGameLayer implements CardTouchListener {

	private Map<CCSprite, Unit> modelMap = new HashMap<CCSprite, Unit>();
	private int xCount;
	private int yCount;
	private final UnitMap<Position, Unit> playerOneMap;
	private final UnitMap<Position, Unit> playerTwoMap;
	private Collection<Action> actions;

	public static CCScene scene(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap) {
		CCScene scene = CCScene.node();
		CCLayer layer = new PlayGameLayer(playerOneMap, playerTwoMap);
		scene.addChild(layer);
		return scene;
	}

	protected PlayGameLayer(UnitMap<Position, Unit> playerOneMap, UnitMap<Position, Unit> playerTwoMap) {

		this.playerOneMap = playerOneMap;
		this.playerTwoMap = playerTwoMap;

		// this.cards = cards;
		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		xCount = 5;
		yCount = 8;

		CCSprite back = CCSprite.sprite("woddenbackground.png");

		back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		addChild(back);

		CCSprite prototype = CCSprite.sprite("archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		tch = new CardTouchHandler();
		tch.addListener(this);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;

		addBackGroundCards(xCount, yCount, true);
		addCards(playerOneMap);
		addCards(playerTwoMap);
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

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			moveCardToOriginalPosition();
		} else {
			moveCardToPosition();
			
			Unit remove = playerOneMap.remove(selectedCard.getUserData());
			if (remove != null) {
				playerOneMap.put(pInP, remove);
			}

			remove = playerTwoMap.remove(selectedCard.getUserData());
			if (remove != null) {
				playerTwoMap.put(pInP, remove);
			}
			
			selectedCard.setUserData(pInP);
		}

		reorderChild(selectedCard, 0);
		selectedCard = null;
	}

	protected void selectCardForMove(CCSprite selectedCard) {
		super.selectCardForMove(selectedCard);

		Unit unit = modelMap.get(selectedCard);

		ActionResolver ar = new ActionResolver(xCount, yCount);

		if (!unit.isEnemy()) {
			actions = ar.getActions(unit, playerOneMap, playerTwoMap);
		} else {
			actions = ar.getActions(unit, playerTwoMap, playerOneMap);
		}

		List<CCNode> children = getChildren();
		for (Action action : actions) {
			for (CCNode ccNode : children) {
				boolean contains = action.getPosition().equals(ccNode.getUserData());
				if (contains) {

					if (action instanceof MoveAction) {
						CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccGREEN);
						ccNode.runAction(tin);
					} else {
						CCTintTo tin = CCTintTo.action(0.2f, ccColor3B.ccRED);
						ccNode.runAction(tin);
					}
				}
			}
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
	}

	@Override
	protected Collection<CCSprite> getCardSprites() {
		return modelMap.keySet();
	}
}
