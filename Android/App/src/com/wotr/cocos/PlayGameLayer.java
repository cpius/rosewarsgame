package com.wotr.cocos;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.layers.CCLayer;
import org.cocos2d.layers.CCScene;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.sound.SoundEngine;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;

import com.wotr.R;
import com.wotr.model.AbstractCard;
import com.wotr.model.Position;
import com.wotr.touch.CardTouchHandler;
import com.wotr.touch.CardTouchListener;

public class PlayGameLayer extends AbstractGameLayer implements CardTouchListener {

	private List<CCSprite> cardList = new ArrayList<CCSprite>();

	public static CCScene scene(Collection<AbstractCard> cards) {
		CCScene scene = CCScene.node();
		CCLayer layer = new PlayGameLayer(cards);
		scene.addChild(layer);
		return scene;
	}

	protected PlayGameLayer(Collection<AbstractCard> cards) {

		// this.cards = cards;
		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		int xCount = 5;
		int yCount = 8;

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
		addCards(cards);
	}

	protected void moveCardToPosition() {
		SoundEngine.sharedEngine().playEffect(CCDirector.sharedDirector().getActivity(), R.raw.pageflip);
		CCScaleTo scaleAction = CCScaleTo.action(0.3f, sizeScale);
		CCSequence seq = CCSequence.actions(scaleAction);
		selectedCard.runAction(seq);
	}

	private void addCards(Collection<AbstractCard> cards) {

		for (AbstractCard card : cards) {
			Position pos = card.getPosistion();
			CGPoint point = bordframe.getPosition(pos.getX(), pos.getY());
			CCSprite player = CCSprite.sprite(card.getImage());
			player.setPosition(point);
			player.setScale(sizeScale);
			addChild(player);
			cardList.add(player);
		}

	}

	@Override
	public void cardDragedEnded(float x, float y) {

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			moveCardToOriginalPosition();
		} else {
			moveCardToPosition();
		}

		reorderChild(selectedCard, 0);
		selectedCard = null;
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
		return cardList;
	}
}
