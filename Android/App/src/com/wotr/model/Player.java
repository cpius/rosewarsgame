package com.wotr.model;

import java.util.Collection;
import java.util.Map;

import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public class Player {

	private Collection<Unit> units;

	public Collection<Unit> getUnits() {
		return units;
	}

	public Player(Collection<Unit> units) {
		this.units = units;
	}

	public Map<Position, Unit> getUnitsMap() {

		Map<Position, Unit> result = new UnitMap<Position, Unit>();
		for (Unit unit : units) {
			result.put(unit.getPosistion(), unit);
		}
		return result;
	}
}
