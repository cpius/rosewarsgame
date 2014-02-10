package com.wotr.cocos;

import java.util.ArrayList;
import java.util.Collection;

import org.cocos2d.actions.instant.CCCallFuncN;
import org.cocos2d.actions.interval.CCMoveTo;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.layers.CCLayer;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.sound.SoundEngine;
import org.cocos2d.types.CGSize;

import com.wotr.R;
import com.wotr.cocos.nodes.UnitBackgroundSprite;
import com.wotr.cocos.nodes.UnitSprite;
import com.wotr.model.Position;

public abstract class AbstractGameLayer extends CCLayer {

	protected Boardframe bordframe;

	protected CGSize winSize;

	protected float sizeScale;

	protected Collection<CCSprite> unitBackgroundList = new ArrayList<CCSprite>();

	protected void selectUnitForMove(CCSprite selectedUnit) {
		CCScaleTo action = CCScaleTo.action(0.2f, sizeScale * 1.5f);
		selectedUnit.runAction(action);
		selectedUnit.setOpacity(130);
	}

	protected void dropUnitToPosition(UnitSprite unit) {
		SoundEngine.sharedEngine().playEffect(CCDirector.sharedDirector().getActivity(), R.raw.pageflip);
		CCScaleTo scaleAction = CCScaleTo.action(0.3f, sizeScale);
		CCCallFuncN sparks = CCCallFuncN.action(this, "spark");
		CCSequence seq = CCSequence.actions(scaleAction, sparks);
		unit.runAction(seq);
	}

	protected void moveUnitToOriginalPosition(UnitSprite unit) {
		CCMoveTo moveAction = CCMoveTo.action(0.4f, unit.getOriginalPosition());
		unit.runAction(moveAction);

		CCScaleTo scaleAction = CCScaleTo.action(0.4f, sizeScale);
		unit.runAction(scaleAction);
	}

	protected void moveUnitToPosition(UnitSprite unit, Position position) {
		CCMoveTo moveAction = CCMoveTo.action(0.4f, bordframe.getPosition(position));
		unit.runAction(moveAction);

		CCScaleTo scaleAction = CCScaleTo.action(0.4f, sizeScale);
		unit.runAction(scaleAction);
	}

	/**
	 * Add the backgound board units to the board
	 * 
	 * @param imagePath
	 * 
	 * @param xCount
	 * @param yCount
	 * @param playBoard
	 */
	protected void addBackGroundUnits(String imagePath, int xCount, int yCount, boolean playBoard) {

		for (int x = 0; x < xCount; x++) {
			for (int y = 0; y < yCount; y++) {

				Position pos = new Position(x, y);

				String imageName = playBoard && y >= yCount / 2 ? "redback.png" : "greenback.png";

				CCSprite unitBackground = new UnitBackgroundSprite(imagePath + imageName, pos, sizeScale, bordframe);
				addChild(unitBackground);
				unitBackgroundList.add(unitBackground);
			}
		}
	}

	protected String getImagePath(CGSize winSize) {

		if (winSize.getHeight() + winSize.getWidth() < 850f) {
			return "small/";
		}
		return "";
	}
}
