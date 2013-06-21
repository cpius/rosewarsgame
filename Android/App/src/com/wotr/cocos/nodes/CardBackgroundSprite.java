package com.wotr.cocos.nodes;

import org.cocos2d.nodes.CCLabel;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.ccColor3B;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;

public class CardBackgroundSprite extends CCSprite {

	public CardBackgroundSprite(String imageName, Position pos, float sizeScale, Boardframe bordframe) {
		super(imageName);

		CGPoint position = bordframe.getPosition(pos);
		setPosition(position);
		setScale(sizeScale * 0.95f);
		setUserData(pos);

		CCLabel posLabel = CCLabel.makeLabel(pos.toString(), "Arial", 20f);
		posLabel.setPosition(position);
		posLabel.setColor(ccColor3B.ccBLACK);
		addChild(posLabel, 100);
	}
}
