package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.UnitType;
import com.wotr.model.unit.Unit;

public class UnitTypeZocBlockStrategy implements ZocBlockStrategy {

	@Override
	public boolean isDirectionBlocked(Unit unit, Direction direction, Position pos, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits) {

		Position[] perpendicularPositions = direction.perpendicular(pos);
		for (Position perpendicularPosition : perpendicularPositions) {
			Unit dUnit = defendingUnits.get(perpendicularPosition);
			if (dUnit != null) {

				for (UnitType zocType : dUnit.getZoc()) {
					if (zocType.equals(unit.getType())) {
						return true;
					}
				}
			}
		}

		return false;
	}
}
