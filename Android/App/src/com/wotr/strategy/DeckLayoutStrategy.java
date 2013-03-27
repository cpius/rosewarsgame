package com.wotr.strategy;

import java.util.Collection;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public interface DeckLayoutStrategy {
	
	UnitMap<Position, Unit> layoutDeck(Collection<Unit> deck);

}
