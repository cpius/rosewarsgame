package com.wotr.cocos.layout.flat;

import org.cocos2d.actions.interval.CCMoveTo;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.types.CGPoint;

import com.wotr.cocos.AbstractGameLayer;
import com.wotr.cocos.nodes.UnitSprite;

public class AbstractGameLayerFlat extends AbstractGameLayer {

	protected void moveUnitToCenterAndEnlarge(UnitSprite unit) {

		unit.setOpacity(255);

		CGPoint center = CGPoint.ccp(winSize.width / 2, winSize.height / 2);

		CCMoveTo moveAction = CCMoveTo.action(0.4f, center);
		unit.runAction(moveAction);

		CCScaleTo scaleAction = CCScaleTo.action(0.4f, sizeScale * 5f);
		unit.runAction(scaleAction);
	}

}
