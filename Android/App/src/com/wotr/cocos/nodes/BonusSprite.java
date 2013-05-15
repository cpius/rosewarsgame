package com.wotr.cocos.nodes;

import org.cocos2d.actions.instant.CCCallback;
import org.cocos2d.actions.interval.CCScaleTo;
import org.cocos2d.actions.interval.CCSequence;
import org.cocos2d.nodes.CCLabel;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.types.ccColor3B;

import com.wotr.cocos.action.ChangeVisibilityNodeCallBackAction;

public class BonusSprite extends CCSprite {

	private final String type;
	private CCLabel label;

	public BonusSprite(float scale, String type) {
		super("bonus-hd.png");
		this.type = type;
		setVisible(false);
		label = CCLabel.makeLabel("+0" + type, "Arial", 30);
		label.setColor(ccColor3B.ccBLACK);

		float y = getContentSize().getHeight() / 2f;
		float x = getContentSize().getWidth() / 2f;
		label.setPosition(x, y);

		addChild(label);
	}

	public void setBonus(int bonusValue) {

		if (bonusValue == 0) {

			ChangeVisibilityNodeCallBackAction cvnca = new ChangeVisibilityNodeCallBackAction(this, false);
			CCCallback callback = CCCallback.action(cvnca);
			CCScaleTo scaleUp = CCScaleTo.action(0.5f, 5f);
			CCScaleTo scaledown = CCScaleTo.action(0.5f, 2f);
			CCSequence seq = CCSequence.actions(scaleUp, scaledown, callback);
			runAction(seq);

		} else {
			label.setString("+" + bonusValue + type);

			ChangeVisibilityNodeCallBackAction cvnca = new ChangeVisibilityNodeCallBackAction(this, true);
			CCCallback callback = CCCallback.action(cvnca);
			CCScaleTo scaleUp = CCScaleTo.action(0.5f, 5f);
			CCScaleTo scaledown = CCScaleTo.action(0.5f, 2f);
			CCSequence seq = CCSequence.actions(callback, scaleUp, scaledown);
			runAction(seq);
		}
	}
}
