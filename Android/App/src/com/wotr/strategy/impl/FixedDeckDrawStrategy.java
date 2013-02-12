package com.wotr.strategy.impl;

import java.util.ArrayList;
import java.util.Collection;

import com.wotr.model.AbstractCard;
import com.wotr.model.Archer;
import com.wotr.model.Ballista;
import com.wotr.model.Catapult;
import com.wotr.model.HeavyCavalry;
import com.wotr.model.LightCavalry;
import com.wotr.model.Pikeman;
import com.wotr.strategy.DeckDrawStrategy;

public class FixedDeckDrawStrategy implements DeckDrawStrategy {

	@Override
	public Collection<AbstractCard> drawDeck() {
		Collection<AbstractCard> result = new ArrayList<AbstractCard>();

		result.add(new Archer());
		result.add(new Archer());
		result.add(new Ballista());
		result.add(new Catapult());
		result.add(new HeavyCavalry());
		result.add(new LightCavalry());
		result.add(new Pikeman());

		return result;
	}

}
