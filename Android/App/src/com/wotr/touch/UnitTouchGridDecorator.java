package com.wotr.touch;

import org.cocos2d.types.CGPoint;

import com.wotr.cocos.Boardframe;
import com.wotr.cocos.nodes.UnitSprite;
import com.wotr.model.Position;

public class UnitTouchGridDecorator implements UnitTouchListener {

	private UnitTouchListener listener;
	private final Boardframe bordframe;

	float lastX, lastY;

	public UnitTouchGridDecorator(Boardframe bordframe) {
		this.bordframe = bordframe;
	}

	@Override
	public boolean unitDragedStarted(UnitSprite unit) {
		return listener.unitDragedStarted(unit);
	}

	@Override
	public void unitDragedEnded(UnitSprite unit, float x, float y) {
		listener.unitDragedEnded(unit, x, y);
	}

	@Override
	public void unitMoved(UnitSprite unit, float x, float y, boolean originalPosition) {
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			listener.unitMoved(unit, x, y, true);
		} else {
			CGPoint position = bordframe.getPosition(pInP.getX(), pInP.getY());
			if (position.x != lastX || position.y != lastY) {
				listener.unitMoved(unit, position.x, position.y, false);
				lastX = position.x;
				lastY = position.y;
			}
		}
	}

	@Override
	public void unitSelected(UnitSprite unit, float x, float y) {
		listener.unitSelected(unit, x, y);
	}

	@Override
	public void unitDeSelected(UnitSprite unit, float x, float y) {
		listener.unitDeSelected(unit, x, y);
	}

	public void addUnitTouchListener(UnitTouchListener listener) {
		this.listener = listener;

	}

}
