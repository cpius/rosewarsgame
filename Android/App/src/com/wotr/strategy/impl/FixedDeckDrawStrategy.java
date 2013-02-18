package com.wotr.strategy.impl;

import java.util.ArrayList;
import java.util.Collection;

import com.wotr.model.unit.Unit;
import com.wotr.model.unit.Archer;
import com.wotr.model.unit.Ballista;
import com.wotr.model.unit.Catapult;
import com.wotr.model.unit.HeavyCavalry;
import com.wotr.model.unit.LightCavalry;
import com.wotr.model.unit.Pikeman;
import com.wotr.strategy.DeckDrawStrategy;

public class FixedDeckDrawStrategy implements DeckDrawStrategy {

	@Override
	public Collection<Unit> drawDeck() {
		Collection<Unit> result = new ArrayList<Unit>();

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
