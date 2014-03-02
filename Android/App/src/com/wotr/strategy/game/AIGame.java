package com.wotr.strategy.game;

import java.util.List;

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.attribute.RawBonus;
import com.wotr.strategy.DeckDrawStrategy;
import com.wotr.strategy.DeckLayoutStrategy;
import com.wotr.strategy.impl.FixedDeckDrawStrategy;
import com.wotr.strategy.impl.RandomDeckLayoutStrategy;
import com.wotr.strategy.player.AIPlayer;

/**
 * AIGame is a game where two bot are playing against each other
 * 
 * @author hansenp
 * 
 */
public class AIGame extends AbstractGame implements Game {

	public AIGame() {

		DeckDrawStrategy deckStrategy = new FixedDeckDrawStrategy();
		List<Unit> deck = deckStrategy.drawDeck(false);

		deck.get(0).getAttackAttribute().addBonus(new RawBonus(1));
		deck.get(1).getDefenceAttribute().addBonus(new RawBonus(1));

		DeckLayoutStrategy layoutStrategy = new RandomDeckLayoutStrategy(getXTileCount(), getYTileCount());
		UnitMap<Position, Unit> layoutDeck = layoutStrategy.layoutDeck(deck);

		playerOne = new AIPlayer(layoutDeck, "Bot 1", 0);

		deckStrategy = new FixedDeckDrawStrategy();
		deck = deckStrategy.drawDeck(true);

		deck.get(0).getAttackAttribute().addBonus(new RawBonus(1));
		deck.get(1).getDefenceAttribute().addBonus(new RawBonus(1));

		layoutStrategy = new RandomDeckLayoutStrategy(getXTileCount(), getYTileCount());
		layoutDeck = layoutStrategy.layoutDeck(deck);

		playerOne = new AIPlayer(layoutDeck, "Bot 2", getYTileCount() - 1);

	}

	@Override
	public boolean isSetup() {
		return true;
	}

}
