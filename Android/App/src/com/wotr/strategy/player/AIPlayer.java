package com.wotr.strategy.player;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public class AIPlayer extends AbstractPlayer implements Player {

	public AIPlayer(UnitMap<Position, Unit> unitMap, String name, int startLine) {
		this.unitMap = unitMap;
		this.name = name;
		this.startLine = startLine;
	}
}
