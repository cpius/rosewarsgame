package com.wotr.cocos;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.cocos2d.layers.CCLayer;
import org.cocos2d.layers.CCScene;
import org.cocos2d.menus.CCMenu;
import org.cocos2d.menus.CCMenuItem;
import org.cocos2d.menus.CCMenuItemImage;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.particlesystem.CCParticleSystem;
import org.cocos2d.particlesystem.CCQuadParticleSystem;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;

import com.google.example.games.basegameutils.GameHelper;
import com.wotr.cocos.nodes.CardSprite;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.attribute.RawBonus;
import com.wotr.strategy.DeckDrawStrategy;
import com.wotr.strategy.DeckLayoutStrategy;
import com.wotr.strategy.impl.FixedDeckDrawStrategy;
import com.wotr.strategy.impl.RandomDeckLayoutStrategy;
import com.wotr.touch.CardTouchGridDecorator;
import com.wotr.touch.CardTouchListener;

public class SetupGameLayer extends AbstractGameLayer implements CardTouchListener {

	// private CCSprite sparkCard;

	private List<CardSprite> cardList = new ArrayList<CardSprite>();
	private Map<CardSprite, Unit> modelMap = new HashMap<CardSprite, Unit>();

	private int xCount;
	private int yCount;
	private GameHelper mHelper;

	public static CCScene scene(GameHelper mHelper) {
		CCScene scene = CCScene.node();
		CCLayer layer = new SetupGameLayer(mHelper);
		scene.addChild(layer);
		return scene;
	}

	protected SetupGameLayer(GameHelper mHelper) {

		this.mHelper = mHelper;
		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		xCount = 5;
		yCount = 4;

		CCSprite back = new CCSprite("woddenbackground.png");

		back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		addChild(back);

		CCSprite prototype = new CCSprite("unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;

		addBackGroundCards(xCount, yCount, false);

		CCMenuItem battleButton = CCMenuItemImage.item("battle.png", "right_arrow.png", this, "startBattle");
		battleButton.setIsEnabled(true);
		battleButton.setVisible(true);

		CGSize battleButtonSize = battleButton.getContentSizeRef();

		addCards();

		CCMenu battleButtonMenu = CCMenu.menu(battleButton);
		battleButtonMenu.setPosition(CGPoint.zero());

		battleButton.setPosition(winSize.getWidth() - battleButtonSize.getWidth() / 2 - 5f, battleButtonSize.getHeight() / 2 + 5f);

		addChild(battleButtonMenu);
	}

	private void addCards() {
		DeckDrawStrategy deckStrategy = new FixedDeckDrawStrategy();
		List<Unit> deck = deckStrategy.drawDeck();

		DeckLayoutStrategy layoutStrategy = new RandomDeckLayoutStrategy(xCount, yCount);
		UnitMap<Position, Unit> layoutDeck = layoutStrategy.layoutDeck(deck);

		CardTouchGridDecorator gridDecorator = new CardTouchGridDecorator(bordframe);
		gridDecorator.addCardTouchListener(this);

		for (Unit unit : layoutDeck.values()) {

			CardSprite card = new CardSprite(unit, sizeScale, bordframe);
			card.addListener(gridDecorator);
			addChild(card);

			cardList.add(card);
			modelMap.put(card, unit);
		}

		deck.get(0).getAttackAttribute().addBonus(new RawBonus(1));
		deck.get(1).getDefenceAttribute().addBonus(new RawBonus(1));
	}

	public void startBattle(Object obj) {

		UnitMap<Position, Unit> playerOnemap = new UnitMap<Position, Unit>();
		for (Unit unit : modelMap.values()) {
			playerOnemap.put(unit.getPosition(), unit);
		}

		UnitMap<Position, Unit> playerTwoMap = playerOnemap.getMirrored(xCount, yCount * 2);

		CCScene scene = PlayGameLayer.scene(playerOnemap, playerTwoMap, mHelper);
		CCDirector.sharedDirector().runWithScene(scene);
	}

	public void spark(Object source) {
		try {
			CCSprite sprite = (CCSprite) source;
			CCParticleSystem particle = new CCQuadParticleSystem("particle/exploding_ring.plist");
			particle.setPosition(sprite.getPosition());
			// particle.setScale(sizeScale);
			addChild(particle);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public boolean cardDragedStarted(CardSprite card) {
		selectCardForMove(card);
		return true;
	}

	@Override
	public void cardDragedEnded(CardSprite card, float x, float y) {

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null || getCardInPosition(pInP) != null) {
			moveCardToOriginalPosition(card);
		} else {
			Unit unit = card.getUnit();
			unit.setPosition(pInP);
			dropCardToPosition(card);
		}

		reorderChild(card, 0);
		card.setOpacity(255);
	}

	@Override
	public void cardMoved(CardSprite card, float x, float y, boolean originalPosition) {
		card.setPosition(x, y);
	}

	private Unit getCardInPosition(Position pInP) {

		for (CardSprite card : cardList) {
			Unit unit = card.getUnit();
			if (pInP.equals(unit.getPosition())) {
				return unit;
			}
		}
		return null;
	}

	@Override
	public void cardSelected(CardSprite card, float x, float y) {
		moveCardToCenterAndEnlarge(card);
	}

	@Override
	public void cardDeSelected(CardSprite card, float x, float y) {
		moveCardToOriginalPosition(card);
	}
}
