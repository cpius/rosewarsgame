package com.wotr.cocos.layout.flat;

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
import com.wotr.cocos.nodes.UnitSprite;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.game.Game;
import com.wotr.touch.UnitTouchGridDecorator;
import com.wotr.touch.UnitTouchListener;

public class SetupGameLayer extends AbstractGameLayerFlat implements UnitTouchListener, BackListener {

	// private CCSprite sparkUnit;

	private List<UnitSprite> unitList = new ArrayList<UnitSprite>();
	private Map<UnitSprite, Unit> modelMap = new HashMap<UnitSprite, Unit>();

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

		// CCSprite back = new CCSprite("woddenbackground.png");

		// back.setPosition(winSize.getWidth() / 2, winSize.getHeight() / 2);
		// addChild(back);

		String imagePath = getImagePath(winSize);

		CCSprite prototype = new CCSprite(imagePath + "unit/archergreen.jpg");
		CGSize contentSize = prototype.getContentSize();
		prototype = null;

		float orientationScale = contentSize.getHeight() / contentSize.getWidth();

		bordframe = new BoardframeFlat(xCount, yCount, winSize.width, winSize.height, 0f, orientationScale, 0.7f);

		sizeScale = bordframe.getLaneWidth() / contentSize.getWidth() * 0.90f;

		addBackGroundUnits(imagePath, xCount, yCount, false);

		CCMenuItem battleButton = CCMenuItemImage.item("battle.png", "right_arrow.png", this, "startBattle");
		battleButton.setIsEnabled(true);
		battleButton.setVisible(true);

		CGSize battleButtonSize = battleButton.getContentSizeRef();

		addUnits(imagePath, game);

		CCMenu battleButtonMenu = CCMenu.menu(battleButton);
		battleButtonMenu.setPosition(CGPoint.zero());

		battleButton.setPosition(winSize.getWidth() - battleButtonSize.getWidth() / 2 - 5f, battleButtonSize.getHeight() / 2 + 5f);

		addChild(battleButtonMenu);
	}

	private void addUnits(String imagePath, Game game) {

		UnitMap<Position, Unit> layoutDeck = game.getAttackingPlayer().getUnitMap();

		UnitTouchGridDecorator gridDecorator = new UnitTouchGridDecorator(bordframe);
		gridDecorator.addUnitTouchListener(this);

		for (Unit unit : layoutDeck.values()) {

			UnitSprite unitSprite = new UnitSprite(imagePath, unit, sizeScale, bordframe);
			unitSprite.addListener(gridDecorator);
			addChild(unitSprite);

			unitList.add(unitSprite);
			modelMap.put(unitSprite, unit);
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
	public boolean unitDragedStarted(UnitSprite unit) {
		selectUnitForMove(unit);
		return true;
	}

	@Override
	public void unitDragedEnded(UnitSprite unitSprite, float x, float y) {

		// If moved to a invalid position move back to original position
		Position pInP = bordframe.getPositionInPerimeter(CGPoint.ccp(x, y));
		if (pInP == null || getUnitInPosition(pInP) != null) {
			moveUnitToOriginalPosition(unitSprite);
		} else {
			Unit unit = unitSprite.getUnit();
			unit.setPosition(pInP);
			dropUnitToPosition(unitSprite);
		}

		reorderChild(unitSprite, 0);
		unitSprite.setOpacity(255);
	}

	@Override
	public void unitMoved(UnitSprite unit, float x, float y, boolean originalPosition) {
		unit.setPosition(x, y);
	}

	private Unit getUnitInPosition(Position pInP) {

		for (UnitSprite unitSprite : unitList) {
			Unit unit = unitSprite.getUnit();
			if (pInP.equals(unit.getPosition())) {
				return unit;
			}
		}
		return null;
	}

	@Override
	public void unitSelected(UnitSprite unit, float x, float y) {
		moveUnitToCenterAndEnlarge(unit);
	}

	@Override
	public void unitDeSelected(UnitSprite unit, float x, float y) {
		moveUnitToOriginalPosition(unit);
	}

	@Override
	public boolean backPressed(SceneManager manager) {

		// TODO Handle boolean
		manager.showMainMenu(true);
		return true;

	}
}
