package com.wotr.cocos.nodes;

import java.util.ArrayList;
import java.util.List;

import org.cocos2d.actions.base.CCRepeatForever;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.events.CCTouchDispatcher;
import org.cocos2d.nodes.CCNode;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.protocols.CCTouchDelegateProtocol;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGRect;

import android.view.MotionEvent;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;
import com.wotr.model.attack.AttackEndPosition;

public class EndPositionSelectionSprite extends CCSprite implements CCTouchDelegateProtocol {

	private final CardSprite card;
	private EndPositionSelectionActionListener listener;

	private static List<EndPositionSelectionSprite> all = new ArrayList<EndPositionSelectionSprite>();

	public EndPositionSelectionSprite(CardSprite card, AttackEndPosition endPosition, float scale, Boardframe bordframe) {
		super("attack_direction-hd.png");
		this.card = card;

		Position position = endPosition.getPosition();

		CGPoint pointPosition = bordframe.getPosition(position);
		setPosition(pointPosition);
		setUserData(endPosition);
		setScale(scale * 2f);

		CCScaleTo scaleUpAction = CCScaleTo.action(0.3f, scale * 1.7f);
		CCScaleTo scaleDownAction = CCScaleTo.action(0.3f, scale * 2.3f);

		CCSequence sequence = CCSequence.actions(scaleUpAction, scaleDownAction);

		CCRepeatForever repeatAction = CCRepeatForever.action(sequence);
		runAction(repeatAction);

		all.add(this);
	}

	public AttackEndPosition getAttackEndPositionUserData() {
		return (AttackEndPosition) getUserData();
	}

	@Override
	public void onEnter() {
		CCTouchDispatcher.sharedDispatcher().addDelegate(this, 10);
		super.onEnter();
	}

	@Override
	public void onExit() {
		CCTouchDispatcher.sharedDispatcher().removeDelegate(this);
		super.onExit();
	}

	@Override
	public boolean ccTouchesBegan(MotionEvent event) {
		CGPoint touchPoint = convertTouchToNodeSpace(event);
		if (CGRect.containsPoint(getTextureRect(), touchPoint)) {
			listener.endPositionSelected(this, card, getAttackEndPositionUserData());

			CCNode parent = getParent();

			for (EndPositionSelectionSprite sprite : all) {
				parent.removeChild(sprite, true);
			}
			all.clear();

			return true;
		}

		return false;
	}

	@Override
	public boolean ccTouchesCancelled(MotionEvent event) {
		return false;
	}

	@Override
	public boolean ccTouchesEnded(MotionEvent event) {
		return false;
	}

	@Override
	public boolean ccTouchesMoved(MotionEvent event) {
		return false;
	}

	public void addActionListener(EndPositionSelectionActionListener listener) {
		this.listener = listener;
	}

}
