package com.wotr.cocos.nodes;

import org.cocos2d.nodes.CCNode;
import org.cocos2d.types.CGPoint;

public class BonusChooserSprite extends CCNode {

	public BonusChooserSprite() {
		super();
		AttackBonusChooserSprite attackBonusChooserSprite = new AttackBonusChooserSprite();
		DefenceBonusChooserSprite defenceBonusChooserSprite = new DefenceBonusChooserSprite();

		setContentSize(attackBonusChooserSprite.getContentSize().width + defenceBonusChooserSprite.getContentSize().getWidth(), attackBonusChooserSprite.getContentSize().getHeight());

		attackBonusChooserSprite.setPosition(CGPoint.ccp(attackBonusChooserSprite.getContentSize().getWidth() / 2f, attackBonusChooserSprite.getContentSize().getHeight() / 2f));
		defenceBonusChooserSprite.setPosition(CGPoint.ccp(attackBonusChooserSprite.getContentSize().getWidth() + defenceBonusChooserSprite.getContentSize().getWidth() / 2f, defenceBonusChooserSprite.getContentSize().getHeight() / 2f));

		setAnchorPoint(0.5f, 0.5f);

		addChild(attackBonusChooserSprite);
		addChild(defenceBonusChooserSprite);
	}
}
