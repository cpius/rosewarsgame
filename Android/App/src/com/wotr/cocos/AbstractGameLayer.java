package com.wotr.cocos;

import java.util.ArrayList;
import java.util.Collection;

import org.cocos2d.actions.instant.CCCallFuncN;
import org.cocos2d.actions.interval.CCMoveTo;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.layers.CCLayer;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.sound.SoundEngine;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;

import com.wotr.R;
import com.wotr.cocos.nodes.CardBackgroundSprite;
import com.wotr.cocos.nodes.CardSprite;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public abstract class AbstractGameLayer extends CCLayer {

	protected Boardframe bordframe;

	protected CGSize winSize;

	protected float sizeScale;

	protected Collection<CCSprite> cardBackgroundList = new ArrayList<CCSprite>();

	// protected abstract Collection<CardSprite> getCardSprites();

	/*
	 * @Override public boolean ccTouchesBegan(MotionEvent event) {
	 * 
	 * for (CardSprite card : getCardSprites()) {
	 * 
	 * if (card.getBoundingBox().contains(event.getRawX(), winSize.height -
	 * event.getRawY())) {
	 * 
	 * boolean cardTouchStarted = isTurn((Unit) card.getUserData()) &&
	 * tch.touchStarted(event.getRawX(), winSize.height - event.getRawY()); if
	 * (cardTouchStarted) { selectedCard = card;
	 * 
	 * if (selectedCard.numberOfRunningActions() == 0) { originalPosition =
	 * selectedCard.getPosition(); } reorderChild(selectedCard, 1);
	 * 
	 * selectCardForMove(selectedCard); } break; } }
	 * 
	 * return super.ccTouchesBegan(event); }
	 */	

	protected void selectCardForMove(CCSprite selectedCard) {
		CCScaleTo action = CCScaleTo.action(0.2f, sizeScale * 1.5f);
		selectedCard.runAction(action);

		selectedCard.setOpacity(130);
	}

	/*
	 * @Override public boolean ccTouchesEnded(MotionEvent event) {
	 * tch.touchEnded(event.getRawX(), winSize.height - event.getRawY()); return
	 * super.ccTouchesEnded(event); }
	 * 
	 * @Override public boolean ccTouchesMoved(MotionEvent event) {
	 * tch.touchMoved(event.getRawX(), winSize.height - event.getRawY()); return
	 * super.ccTouchesMoved(event); }
	 */

	protected void moveCardToCenterAndEnlarge(CardSprite unit) {

		unit.setOpacity(255);

		CGPoint center = CGPoint.ccp(winSize.width / 2, winSize.height / 2);

		CCMoveTo moveAction = CCMoveTo.action(0.4f, center);
		unit.runAction(moveAction);

		CCScaleTo scaleAction = CCScaleTo.action(0.4f, sizeScale * 5f);
		unit.runAction(scaleAction);
	}

	protected void dropCardToPosition(CardSprite card) {
		SoundEngine.sharedEngine().playEffect(CCDirector.sharedDirector().getActivity(), R.raw.pageflip);
		CCScaleTo scaleAction = CCScaleTo.action(0.3f, sizeScale);
		CCCallFuncN sparks = CCCallFuncN.action(this, "spark");
		CCSequence seq = CCSequence.actions(scaleAction, sparks);
		card.runAction(seq);
	}

	protected void moveCardToOriginalPosition(CardSprite card) {
		CCMoveTo moveAction = CCMoveTo.action(0.4f, card.getOriginalPosition());
		card.runAction(moveAction);

		CCScaleTo scaleAction = CCScaleTo.action(0.4f, sizeScale);
		card.runAction(scaleAction);
	}

	protected void moveCardToPosition(CardSprite card, Position position) {
		CCMoveTo moveAction = CCMoveTo.action(0.4f, bordframe.getPosition(position));
		card.runAction(moveAction);

		CCScaleTo scaleAction = CCScaleTo.action(0.4f, sizeScale);
		card.runAction(scaleAction);
	}

	/**
	 * Add the backgound board cards to the board
	 * 
	 * @param imagePath
	 * 
	 * @param xCount
	 * @param yCount
	 * @param playBoard
	 */
	protected void addBackGroundCards(String imagePath, int xCount, int yCount, boolean playBoard) {

		for (int x = 0; x < xCount; x++) {
			for (int y = 0; y < yCount; y++) {

				Position pos = new Position(x, y);

				String imageName = playBoard && y >= yCount / 2 ? "redback.png" : "greenback.png";

				CCSprite cardBackground = new CardBackgroundSprite(imagePath + imageName, pos, sizeScale, bordframe);
				addChild(cardBackground);
				cardBackgroundList.add(cardBackground);
			}
		}
	}
	
	protected String getImagePath(CGSize winSize) {
		
		if(winSize.getHeight() + winSize.getWidth() < 850f) {
			return "small/";
		}
		return "";
	}
}
