package com.wotr.touch;

import com.wotr.cocos.nodes.CardSprite;

public interface CardTouchListener {

	boolean cardDragedStarted(CardSprite card);
	
	void cardDragedEnded(CardSprite card, float x, float y);

	void cardMoved(CardSprite card, float x, float y, boolean originalPosition);

	void cardSelected(CardSprite card, float x, float y);

	void cardDeSelected(CardSprite card, float x, float y);
}
