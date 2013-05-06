package com.wotr.cocos.nodes;

import org.cocos2d.actions.base.CCRepeatForever;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.types.CGPoint;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;

public class GoSprite extends CCSprite {

	public GoSprite(Position position, float scale, Boardframe bordframe) {
		super("attack_direction-hd.png");

		CGPoint pointPosition = bordframe.getPosition(position);
		setPosition(pointPosition);
		setUserData(position);
		setScale(scale * 2f);
	
		CCScaleTo scaleUpAction = CCScaleTo.action(0.3f, scale * 1.7f);
		CCScaleTo scaleDownAction = CCScaleTo.action(0.3f, scale * 2.3f);
				
		CCSequence sequence = CCSequence.actions(scaleUpAction, scaleDownAction);
		
		CCRepeatForever repeatAction = CCRepeatForever.action(sequence);	
		runAction(repeatAction);
	}
	
	public Position getPositionUserData() {
		return (Position) getUserData();
	}
}
