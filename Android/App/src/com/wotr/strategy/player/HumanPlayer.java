package com.wotr.strategy.player;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public class HumanPlayer extends AbstractPlayer implements Player {

	public HumanPlayer(UnitMap<Position, Unit> unitMap, String name, int startLine) {
		this.unitMap = unitMap;
		this.name = name;
		this.startLine = startLine;
	}
	
	@Override
	public boolean canAttack() {
		return true;
	}
}
