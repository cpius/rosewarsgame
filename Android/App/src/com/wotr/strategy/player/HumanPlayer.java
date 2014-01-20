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
	public String getName() {
		return name;
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

}
