package com.wotr.strategy.action;

import java.util.Map;

import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public interface ZocBlockStrategy {

	boolean isDirectionBlocked(Unit unit, Direction d, Position pos, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits);

}
