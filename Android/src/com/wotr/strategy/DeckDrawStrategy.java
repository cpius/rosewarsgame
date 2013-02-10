package com.wotr.strategy;

import java.util.Collection;

import com.wotr.model.AbstractCard;

public interface DeckDrawStrategy {
	
	public Collection<AbstractCard> drawDeck();

}
