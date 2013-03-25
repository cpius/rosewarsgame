package com.wotr.strategy.player;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public class HumanPlayer extends AbstractPlayer implements Player {

	private final UnitMap<Position, Unit> unitMap;

	private final String name;

	public HumanPlayer(UnitMap<Position, Unit> unitMap, String name) {
		this.unitMap = unitMap;
		this.name = name;
	}

	@Override
	public String getName() {
		return name;
	}

	public UnitMap<Position, Unit> getUnitMap() {
		return unitMap;
	}

}
