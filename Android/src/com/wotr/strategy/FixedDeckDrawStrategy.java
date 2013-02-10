package com.wotr.strategy;

import java.util.ArrayList;
import java.util.Collection;

import com.wotr.model.AbstractCard;
import com.wotr.model.Archer;
import com.wotr.model.Ballista;
import com.wotr.model.Catapult;
import com.wotr.model.Heavycavalry;
import com.wotr.model.Lightcavalry;
import com.wotr.model.Pikeman;

public class FixedDeckDrawStrategy implements DeckDrawStrategy {

	@Override
	public Collection<AbstractCard> drawDeck() {
		Collection<AbstractCard> result = new ArrayList<AbstractCard>();

		result.add(new Archer());
		result.add(new Archer());
		result.add(new Ballista());
		result.add(new Catapult());
		result.add(new Heavycavalry());
		result.add(new Lightcavalry());
		result.add(new Pikeman());

		return result;
	}

}
