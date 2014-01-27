package com.wotr.cocos;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.cocos2d.menus.CCMenu;
import org.cocos2d.menus.CCMenuItem;
import org.cocos2d.menus.CCMenuItemImage;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.particlesystem.CCParticleSystem;
import org.cocos2d.particlesystem.CCQuadParticleSystem;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;

import android.content.Context;

import com.wotr.BackListener;
import com.wotr.SceneManager;
import com.wotr.cocos.nodes.CardSprite;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.game.Game;
import com.wotr.touch.CardTouchGridDecorator;
import com.wotr.touch.CardTouchListener;

public class SetupGameLayer extends AbstractGameLayer implements CardTouchListener, BackListener {

	// private CCSprite sparkCard;

	private List<CardSprite> cardList = new ArrayList<CardSprite>();
	private Map<CardSprite, Unit> modelMap = new HashMap<CardSprite, Unit>();

	private int xCount;
	private int yCount;
	private SceneManager sceneManager;
	private Game game;

	public SetupGameLayer(Context context, SceneManager sceneManager, Game game) {

		this.sceneManager = sceneManager;
		this.game = game;
		setIsTouchEnabled(true);

		winSize = CCDirector.sharedDirector().displaySize();

		xCount = game.getXTileCount();
		yCount = game.getYTileCount();

		//CCSprite back = new CCSprite("woddenbackground.png");

		//back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		//addChild(back);

		String imagePath = getImagePath(winSize);
		
		CCSprite prototype = new CCSprite(imagePath + "unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();
		prototype = null;

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new Boardframe(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;		
		
		addBackGroundCards(imagePath, xCount, yCount, false);

		CCMenuItem battleButton = CCMenuItemImage.item("battle.png", "right_arrow.png", this, "startBattle");
		battleButton.setIsEnabled(true);
		battleButton.setVisible(true);

		CGSize battleButtonSize = battleButton.getContentSizeRef();

		addCards(imagePath, game);

		CCMenu battleButtonMenu = CCMenu.menu(battleButton);
		battleButtonMenu.setPosition(CGPoint.zero());

		battleButton.setPosition(winSize.getWidth() - battleButtonSize.getWidth() / 2 - 5f, battleButtonSize.getHeight() / 2 + 5f);

		addChild(battleButtonMenu);
	}	

	private void addCards(String imagePath, Game game) {

		UnitMap<Position, Unit> layoutDeck = game.getAttackingPlayer().getUnitMap();

		CardTouchGridDecorator gridDecorator = new CardTouchGridDecorator(bordframe);
		gridDecorator.addCardTouchListener(this);

		for (Unit unit : layoutDeck.values()) {

			CardSprite card = new CardSprite(imagePath, unit, sizeScale, bordframe);
			card.addListener(gridDecorator);
			addChild(card);

			cardList.add(card);
			modelMap.put(card, unit);
		}

	}

	public void startBattle(Object obj) {
		game.setupDone(game.getAttackingPlayer());
		sceneManager.showMatch(game);
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

	@Override
	public boolean backPressed(SceneManager manager) {

		// TODO Handle boolean
		manager.showMainMenu(true);
		return true;

	}
}
