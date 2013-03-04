package com.wotr.cocos;

import java.util.ArrayList;
import java.util.Collection;
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

import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.DeckDrawStrategy;
import com.wotr.strategy.impl.FixedDeckDrawStrategy;
import com.wotr.touch.CardTouchHandler;
import com.wotr.touch.CardTouchListener;

public class SetupGameLayer extends AbstractGameLayer implements CardTouchListener {

	private CCSprite sparkCard;

	private List<CCSprite> cardList = new ArrayList<CCSprite>();
	private Map<CCSprite, Unit> modelMap = new HashMap<CCSprite, Unit>();

	private int xCount;
	private int yCount;

	public static CCScene scene() {
		CCScene scene = CCScene.node();
		CCLayer layer = new SetupGameLayer();
		scene.addChild(layer);
		return scene;
	}

	protected SetupGameLayer() {

		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		xCount = 5;
		yCount = 4;

		CCSprite back = CCSprite.sprite("woddenbackground.png");

		back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		addChild(back);

		CCSprite prototype = CCSprite.sprite("unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		tch = new CardTouchHandler();
		tch.addListener(this);

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
		DeckDrawStrategy deck = new FixedDeckDrawStrategy();
		Collection<Unit> drawDeck = deck.drawDeck();
		for (Unit unit : drawDeck) {
			CGPoint position = CGPoint.ccp(100, 100);
			CCSprite player = CCSprite.sprite(unit.getImage());
			player.setPosition(position);
			player.setScale(sizeScale);
			addChild(player);

			cardList.add(player);

			modelMap.put(player, unit);
		}
	}

	public void startBattle(Object obj) {

		UnitMap<Position, Unit> playerOnemap = new UnitMap<Position, Unit>();
		for (Unit unit : modelMap.values()) {
			playerOnemap.put(unit.getPosistion(), unit);
		}

		UnitMap<Position, Unit> playerTwoMap = playerOnemap.getMirrored(xCount, yCount * 2);

		CCScene scene = PlayGameLayer.scene(playerOnemap, playerTwoMap);
		CCDirector.sharedDirector().runWithScene(scene);
	}

	public void spark() {
		try {
			CCParticleSystem particle = new CCQuadParticleSystem("particle/exploding_ring.plist");
			particle.setPosition(sparkCard.getPosition());
			//particle.setScale(sizeScale);
			addChild(particle);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Override
	public void cardDragedEnded(float x, float y) {

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null || getCardInPosition(pInP) != null) {
			moveCardToOriginalPosition();
		} else {
			moveCardToPosition();
			Unit abstractCard = modelMap.get(selectedCard);
			abstractCard.setPosistion(pInP);
		}
		sparkCard = selectedCard;

		reorderChild(selectedCard, 0);
		selectedCard = null;
	}

	@Override
	public void cardMoved(float x, float y) {
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null) {
			selectedCard.setPosition(x, y);
		} else {
			CGPoint position = bordframe.getPosition(pInP.getX(), pInP.getY());
			selectedCard.setPosition(position);			
		}
	}

	private Unit getCardInPosition(Position pInP) {
		Collection<Unit> values = modelMap.values();
		for (Unit card : values) {
			if (pInP.equals(card.getPosistion())) {
				return card;
			}
		}
		return null;
	}

	@Override
	public void cardSelected(float x, float y) {
		moveCardToCenterAndEnlarge();
	}

	@Override
	public void cardDeSelected(float x, float y) {
		moveCardToOriginalPosition();
	}

	@Override
	protected Collection<CCSprite> getCardSprites() {
		return cardList;
	}
}
