package com.wotr.strategy.player;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public abstract class AbstractPlayer implements Player {

	protected UnitMap<Position, Unit> unitMap = null;
	protected int startLine;

	protected String name = null;
	
	@Override
	public String getName() {
		return "PlayerName";
	}
	
	public UnitMap<Position, Unit> getUnitMap() {
		return unitMap;
	}

	@Override
	public boolean hasUnitAtPosition(Position pInP) {
		return getUnitMap().containsKey(pInP);
	}

	@Override
	public Unit getUnitAtPosition(Position pInP) {
		return getUnitMap().get(pInP);
	}

	@Override
	public boolean hasUnit(Unit unit) {
		return getUnitMap().containsValue(unit);
	}	

	public int getStartLine() {
		return startLine;
	}

}
