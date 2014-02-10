package com.wotr.cocos.nodes;

import com.wotr.model.attack.AttackEndPosition;

public interface EndPositionSelectionActionListener {

	void endPositionSelected(EndPositionSelectionSprite goSprite, UnitSprite card, AttackEndPosition endPosition);

}
