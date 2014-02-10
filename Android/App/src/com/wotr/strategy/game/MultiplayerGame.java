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
import com.wotr.strategy.player.HumanPlayer;

/**
 * A multiplayer game is a game where two human players are playing against each
 * other on the same device.
 * 
 * @author hansenp
 * 
 */
public class MultiplayerGame extends AbstractGame implements Game {

	private int setupCount = 0;

	public MultiplayerGame() {
		DeckDrawStrategy deckStrategy = new FixedDeckDrawStrategy();
		List<Unit> deck = deckStrategy.drawDeck();

		deck.get(0).getAttackAttribute().addBonus(new RawBonus(1));
		deck.get(1).getDefenceAttribute().addBonus(new RawBonus(1));

		DeckLayoutStrategy layoutStrategy = new RandomDeckLayoutStrategy(getXTileCount(), getYTileCount());
		UnitMap<Position, Unit> layoutDeck = layoutStrategy.layoutDeck(deck);

		playerOne = new HumanPlayer(layoutDeck, "Player 1", 0);

		deckStrategy = new FixedDeckDrawStrategy();
		deck = deckStrategy.drawDeck();

		deck.get(0).getAttackAttribute().addBonus(new RawBonus(1));
		deck.get(1).getDefenceAttribute().addBonus(new RawBonus(1));

		layoutStrategy = new RandomDeckLayoutStrategy(getXTileCount(), getYTileCount());
		layoutDeck = layoutStrategy.layoutDeck(deck);

		playerTwo = new HumanPlayer(layoutDeck, "Player 2", (getYTileCount() * 2) - 1);

		// First player to setup is the first one
		currentPlayer = playerOne;
	}

	@Override
	public boolean isSetup() {

		if (setupCount == 1) {
			// It this time playerOne has setup - playerTwo is now up.
			currentPlayer = playerTwo;
		}

		if (setupCount++ > 1) {
			playerTwo.getUnitMap().mirrorUnits(getXTileCount(), getYTileCount() * 2);
			currentPlayer = playerOne;
			return true;
		}

		return false;

	}

	@Override
	/**
	 * Set initial number of actions
	 */
	public int getRemainingActions() {
		return 1;
	}
}
