package com.wotr.touch;

import com.wotr.cocos.nodes.UnitSprite;

public interface UnitTouchListener {

	boolean unitDragedStarted(UnitSprite unit);
	
	void unitDragedEnded(UnitSprite unit, float x, float y);

	void unitMoved(UnitSprite unit, float x, float y, boolean originalPosition);

	void unitSelected(UnitSprite unit, float x, float y);

	void unitDeSelected(UnitSprite unit, float x, float y);
}
