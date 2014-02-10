package com.wotr.cocos.nodes;

import org.cocos2d.events.CCTouchDispatcher;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.protocols.CCTouchDelegateProtocol;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGRect;
import org.cocos2d.types.CGSize;

import android.view.MotionEvent;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.attribute.BonusListener;
import com.wotr.touch.UnitTouchListener;

public class UnitSprite extends CCSprite implements BonusListener, CCTouchDelegateProtocol {

	private static final long BUTTON_TIME = 500;

	private BonusSprite attackBonus;
	private BonusSprite defenceBonus;
	private UnitTouchListener listener;

	private static UnitSprite activeCard;
	private boolean detailed = false;

	// Is only used to calculate if unit is moved
	private float startTouchPointX;
	private float startTouchPointY;

	private CGPoint originalCardPosition;

	private long startTime;

	public UnitSprite(String imagePath, Unit unit, float scale, Boardframe bordframe) {
		super(imagePath + unit.getImage());

		Position pos = unit.getPosition();
		CGPoint point = bordframe.getPosition(pos.getX(), pos.getY());
		setPosition(point);
		setScale(scale);
		setUserData(unit);

		unit.getAttackAttribute().addBonusListener(this);
		unit.getDefenceAttribute().addBonusListener(this);

		CGSize cardSize = getContentSize();

		attackBonus = new BonusSprite(scale, "A");
		CGSize bonusSize = attackBonus.getContentSize();

		attackBonus.setPosition(bonusSize.getWidth(), cardSize.getHeight() - bonusSize.getHeight());
		defenceBonus = new BonusSprite(scale, "D");
		defenceBonus.setPosition(bonusSize.getWidth(), cardSize.getHeight() - bonusSize.getHeight() * 3);

		addChild(attackBonus);
		addChild(defenceBonus);
	}

	public Unit getUnit() {
		return (Unit) getUserData();
	}

	@Override
	public void attackBonusChanged(int bonusValue) {
		attackBonus.setBonus(bonusValue);
	}

	@Override
	public void defenceBonusChanged(int bonusValue) {
		defenceBonus.setBonus(bonusValue);
	}

	public void drawBonus() {
		attackBonus.setBonus(getUnit().getAttackAttribute().getBonusValue());
		defenceBonus.setBonus(getUnit().getDefenceAttribute().getBonusValue());
	}

	@Override
	public void onEnter() {
		CCTouchDispatcher.sharedDispatcher().addDelegate(this, 100);
		super.onEnter();
	}

	@Override
	public void onExit() {
		CCTouchDispatcher.sharedDispatcher().removeDelegate(this);
		super.onExit();
	}

	@Override
	public boolean ccTouchesBegan(MotionEvent event) {

		// There is already another active card
		if (activeCard != null && !this.equals(activeCard)) {
			return false;
		}

		CGPoint touchPoint = convertTouchToNodeSpace(event);
		if (CGRect.containsPoint(getTextureRect(), touchPoint)) {

			startTouchPointX = event.getRawX();
			startTouchPointY = event.getRawY();

			startTime = System.currentTimeMillis();

			if (!detailed && listener.unitDragedStarted(this)) {
				activeCard = this;
				originalCardPosition = getPosition();
			}

			return true;
		}
		return false;
	}

	@Override
	public boolean ccTouchesEnded(MotionEvent event) {

		// this card is not the active
		if (!this.equals(activeCard)) {
			return false;
		}

		CGPoint touchPoint = convertTouchToNodeSpace(event);
		if (CGRect.containsPoint(getTextureRect(), touchPoint)) {

			long duration = System.currentTimeMillis() - startTime;

			boolean hasMoved = hasMoved(event.getRawX(), event.getRawY(), startTouchPointX, startTouchPointY);
			boolean buttonPressTime = duration < BUTTON_TIME;

			// Pressed like a button
			if (buttonPressTime && !hasMoved) {

				if (detailed) {
					activeCard = null;
					detailed = !detailed;
					listener.unitDeSelected(this, originalCardPosition.x, originalCardPosition.y);
				} else {
					detailed = !detailed;
					listener.unitSelected(this, originalCardPosition.x, originalCardPosition.y);
				}

			} else if (!detailed) {
				CCDirector sd = CCDirector.sharedDirector();
				CGSize displaySize = sd.displaySize();
				listener.unitDragedEnded(this, event.getX(), displaySize.getHeight() - event.getY());
				activeCard = null;
			}

			return true;
		}

		return false;
	}

	@Override
	public boolean ccTouchesMoved(MotionEvent event) {

		// this card is not the active
		if (!this.equals(activeCard)) {
			return false;
		}

		// If card is not showing details, move the card
		if (!detailed) {
			CCDirector sd = CCDirector.sharedDirector();
			CGSize displaySize = sd.displaySize();
			listener.unitMoved(this, event.getX(), displaySize.getHeight() - event.getY(), true);
		}

		return true;
	}

	public void addListener(UnitTouchListener listener) {
		this.listener = listener;
	}

	// If length between the two points is more thart 60 pixels
	private boolean hasMoved(float touchX, float touchY, float startX, float startY) {
		float move = Math.abs(touchX - startX) + Math.abs(touchY - startY);
		boolean moved = move > 60;
		return moved;
	}

	public CGPoint getOriginalPosition() {
		return originalCardPosition;
	}

	@Override
	public boolean ccTouchesCancelled(MotionEvent event) {
		return this.equals(activeCard);
	}
}
