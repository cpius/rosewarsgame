package com.wotr.touch;

import org.cocos2d.types.CGPoint;

import com.wotr.cocos.Boardframe;
import com.wotr.cocos.nodes.CardSprite;
import com.wotr.model.Position;

public class CardTouchGridDecorator implements CardTouchListener {

	private CardTouchListener listener;
	private final Boardframe bordframe;
	
	float lastX, lastY;

	public CardTouchGridDecorator(Boardframe bordframe) {
		this.bordframe = bordframe;
	}

	@Override
	public boolean cardDragedStarted(CardSprite card) {
		return listener.cardDragedStarted(card);
	}

	@Override
	public void cardDragedEnded(CardSprite card, float x, float y) {
		listener.cardDragedEnded(card, x, y);

	}

	@Override
	public void cardMoved(CardSprite card, float x, float y, boolean originalPosition) {
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			listener.cardMoved(card, x, y, true);
		} else {
			CGPoint position = bordframe.getPosition(pInP.getX(), pInP.getY());
			if(position.x != lastX ||  position.y != lastY) {
				listener.cardMoved(card, position.x, position.y, false);
				lastX = position.x;
				lastY = position.y;
			}
		}		
	}

	@Override
	public void cardSelected(CardSprite card, float x, float y) {
		listener.cardSelected(card, x, y);
	}

	@Override
	public void cardDeSelected(CardSprite card, float x, float y) {
		listener.cardDeSelected(card, x, y);
	}

	public void addCardTouchListener(CardTouchListener listener) {
		this.listener = listener;

	}

}
