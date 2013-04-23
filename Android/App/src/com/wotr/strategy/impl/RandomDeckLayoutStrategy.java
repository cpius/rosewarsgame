package com.wotr.strategy.impl;

import java.util.Arrays;
import java.util.Collection;
import java.util.List;
import java.util.Random;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.basic.Archer;
import com.wotr.model.unit.basic.Ballista;
import com.wotr.model.unit.basic.Catapult;
import com.wotr.model.unit.basic.LightCavalry;
import com.wotr.model.unit.basic.Pikeman;
import com.wotr.strategy.DeckLayoutStrategy;

public class RandomDeckLayoutStrategy implements DeckLayoutStrategy {

	private final int xCount;
	private final int yCount;

	@SuppressWarnings("unchecked")
	private List<Class<Pikeman>> nonBackLineUnits = Arrays.asList(Pikeman.class);

	@SuppressWarnings("unchecked")
	private List<Class<? extends Unit>> nonFrontLineUnits = Arrays.asList(LightCavalry.class, Ballista.class, Catapult.class, Archer.class);

	// _nonFrontLineUnits = @[@(kLightCavalry), @(kBallista), @(kCatapult), //
	// @(kArcher), @(kScout), @(kSaboteur), @(kDiplomat), @(kBerserker),//
	// @(kCannon), @(kWeaponSmith), @(kRoyalGuard)];
	// _nonBackLineUnits = @[@(kPikeman), @(kBerserker), @(kLongSwordsMan), //
	// @(kRoyalGuard), @(kSamurai), @(kViking), @(kWarElephant)];

	public RandomDeckLayoutStrategy(int xCount, int yCount) {
		this.xCount = xCount;
		this.yCount = yCount;
	}

	@Override
	public UnitMap<Position, Unit> layoutDeck(Collection<Unit> deck) {

		while (true) {
			UnitMap<Position, Unit> placedDeck = placeCardsInDeck(deck);

			if (validateDeck(placedDeck)) {
				return placedDeck;
			}
		}
	}

	UnitMap<Position, Unit> placeCardsInDeck(Collection<Unit> deck) {

		UnitMap<Position, Unit> result = new UnitMap<Position, Unit>();

		Random random = new Random();

		for (Unit unit : deck) {
			boolean cardInValidPosition = false;

			while (!cardInValidPosition) {

				int x = random.nextInt(xCount);
				int y = random.nextInt(yCount);

				Position position = new Position(x, y);
				if (!result.containsKey(position)) {
					result.put(position, unit);
					cardInValidPosition = true;
				}
			}
		}
		return result;
	}

	private boolean validateDeck(UnitMap<Position, Unit> placedDeck) {
		return deckContainsNoNonFrontLineUnitInFrontLine(placedDeck) && deckContainsNoBackLineUnitsInBackLine(placedDeck) && deckContainsMoreThanOneUnitOnBackLine(placedDeck) && deckContainsMaxOnePikemanPerColumn(placedDeck);
	}

	private boolean deckContainsNoNonFrontLineUnitInFrontLine(UnitMap<Position, Unit> placedDeck) {

		for (Unit unit : placedDeck.values()) {
			if (unit.getPosition().getY() == yCount - 1 && nonFrontLineUnits.contains(unit.getClass())) {
				return false;
			}
		}

		return true;
	}

	private boolean deckContainsNoBackLineUnitsInBackLine(UnitMap<Position, Unit> placedDeck) {

		for (Unit unit : placedDeck.values()) {
			if (unit.getPosition().getY() == 0 && nonBackLineUnits.contains(unit.getClass())) {
				return false;
			}
		}

		return true;
	}

	private boolean deckContainsMoreThanOneUnitOnBackLine(UnitMap<Position, Unit> placedDeck) {

		int unitsOnBackLine = 0;

		for (Unit unit : placedDeck.values()) {
			if (unit.getPosition().getY() == 0) {
				unitsOnBackLine++;
			}
		}

		return unitsOnBackLine > 1;
	}

	private boolean deckContainsMaxOnePikemanPerColumn(UnitMap<Position, Unit> placedDeck) {

		int pikemen = 0;

		for (int column = 1; column <= xCount; column++) {
			for (int row = 1; row <= yCount; row++) {

				Unit unit = placedDeck.get(new Position(row, column));
				if (unit != null && unit instanceof Pikeman) {
					pikemen++;

					if (pikemen == 2) {
						return false;
					}
				}
			}

			pikemen = 0;
		}

		return true;
	}
}
