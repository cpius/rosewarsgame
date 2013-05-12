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

public class GoSprite extends CCSprite implements CCTouchDelegateProtocol {

	private final CardSprite card;
	private GoSpriteActionLisener listener;

	private static List<GoSprite> all = new ArrayList<GoSprite>();

	public GoSprite(CardSprite card, Position position, float scale, Boardframe bordframe) {
		super("attack_direction-hd.png");
		this.card = card;

		CGPoint pointPosition = bordframe.getPosition(position);
		setPosition(pointPosition);
		setUserData(position);
		setScale(scale * 2f);

		CCScaleTo scaleUpAction = CCScaleTo.action(0.3f, scale * 1.7f);
		CCScaleTo scaleDownAction = CCScaleTo.action(0.3f, scale * 2.3f);

		CCSequence sequence = CCSequence.actions(scaleUpAction, scaleDownAction);

		CCRepeatForever repeatAction = CCRepeatForever.action(sequence);
		runAction(repeatAction);

		all.add(this);
	}

	public Position getPositionUserData() {
		return (Position) getUserData();
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
			listener.goSpriteSpressed(this, card, getPositionUserData());

			CCNode parent = getParent();
			
			for (GoSprite sprite : all) {
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

	public void addActionListener(GoSpriteActionLisener listener) {
		this.listener = listener;
	}

}
