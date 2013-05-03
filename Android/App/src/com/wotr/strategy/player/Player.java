package com.wotr.strategy.player;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public interface Player {

	String getName();

	UnitMap<Position, Unit> getUnitMap();

	boolean hasUnitAtPosition(Position pInP);

	Unit getUnitAtPosition(Position pInP);

	boolean hasUnit(Unit unit);

	int getStartLine();

}
