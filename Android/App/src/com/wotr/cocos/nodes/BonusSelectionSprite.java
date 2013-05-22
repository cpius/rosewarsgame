package com.wotr.cocos.nodes;

import java.util.Collection;

import org.cocos2d.events.CCTouchDispatcher;
import org.cocos2d.nodes.CCNode;
import org.cocos2d.protocols.CCTouchDelegateProtocol;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGRect;

import android.view.MotionEvent;

import com.wotr.model.unit.attribute.bonus.AttackBonusAward;
import com.wotr.model.unit.attribute.bonus.BonusAward;
import com.wotr.model.unit.attribute.bonus.DefenceBonusAward;

public class BonusSelectionSprite extends CCNode implements CCTouchDelegateProtocol {

	private BonusSelectionActionListener listener;
	private AttackBonusSelectionSprite attackBonusChooserSprite;
	private DefenceBonusSelectionSprite defenceBonusChooserSprite;

	public BonusSelectionSprite(Collection<BonusAward> awardProspects) {
		super();
		attackBonusChooserSprite = new AttackBonusSelectionSprite();
		defenceBonusChooserSprite = new DefenceBonusSelectionSprite();

		setContentSize(attackBonusChooserSprite.getContentSize().width + defenceBonusChooserSprite.getContentSize().getWidth(), attackBonusChooserSprite.getContentSize().getHeight());

		attackBonusChooserSprite.setPosition(CGPoint.ccp(attackBonusChooserSprite.getContentSize().getWidth() / 2f, attackBonusChooserSprite.getContentSize().getHeight() / 2f));
		defenceBonusChooserSprite.setPosition(CGPoint.ccp(attackBonusChooserSprite.getContentSize().getWidth() + defenceBonusChooserSprite.getContentSize().getWidth() / 2f, defenceBonusChooserSprite.getContentSize().getHeight() / 2f));

		setAnchorPoint(0.5f, 0.5f);

		for (BonusAward bonusAward : awardProspects) {
			if (bonusAward instanceof AttackBonusAward) {
				attackBonusChooserSprite.setBonusAward(bonusAward);
			} else if (bonusAward instanceof DefenceBonusAward) {
				defenceBonusChooserSprite.setBonusAward(bonusAward);
			}

		}

		addChild(attackBonusChooserSprite);
		addChild(defenceBonusChooserSprite);
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
		if (CGRect.containsPoint(attackBonusChooserSprite.getTextureRect(), touchPoint)) {
			touch(attackBonusChooserSprite);
		} else if (CGRect.containsPoint(defenceBonusChooserSprite.getTextureRect(), touchPoint)) {
			touch(defenceBonusChooserSprite);
		}

		return true;
	}

	private void touch(AbstractBonusSelectionSprite bsp) {
		BonusAward bonusAward = bsp.getBonusAward();

		if (bonusAward != null) {
			listener.bonusSelected(bonusAward);
			getParent().removeChild(this, true);
		}

	}

	@Override
	public boolean ccTouchesCancelled(MotionEvent arg0) {
		return false;
	}

	@Override
	public boolean ccTouchesEnded(MotionEvent arg0) {
		return false;
	}

	@Override
	public boolean ccTouchesMoved(MotionEvent arg0) {
		return false;
	}

	public void addActionListener(BonusSelectionActionListener listener) {
		this.listener = listener;
	}

}
