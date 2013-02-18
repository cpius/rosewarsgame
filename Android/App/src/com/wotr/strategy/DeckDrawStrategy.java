package com.wotr.strategy;

import java.util.Collection;

import com.wotr.model.unit.Unit;

public interface DeckDrawStrategy {
	
	public Collection<Unit> drawDeck();

}
