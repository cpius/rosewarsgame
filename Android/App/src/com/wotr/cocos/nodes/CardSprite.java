package com.wotr.cocos.nodes;

import org.cocos2d.nodes.CCSprite;
import org.cocos2d.types.CGPoint;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public class CardSprite extends CCSprite {

	public CardSprite(Unit card, float scale, Boardframe bordframe) {
		super(card.getImage());
		
		Position pos = card.getPosition();
		CGPoint point = bordframe.getPosition(pos.getX(), pos.getY());
		setPosition(point);
		setScale(scale);
		setUserData(card);
	}
}
