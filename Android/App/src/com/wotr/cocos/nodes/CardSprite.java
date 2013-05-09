package com.wotr.cocos.nodes;

import org.cocos2d.nodes.CCSprite;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.attribute.BonusListener;

public class CardSprite extends CCSprite implements BonusListener {

	private BonusSprite attackBonus;
	private BonusSprite defenceBonus;
	private final Unit unit;

	public CardSprite(Unit unit, float scale, Boardframe bordframe) {
		super(unit.getImage());
		this.unit = unit;

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

	@Override
	public void attackBonusChanged(int bonusValue) {
		attackBonus.setBonus(bonusValue);
	}

	@Override
	public void defenceBonusChanged(int bonusValue) {
		defenceBonus.setBonus(bonusValue);
	}
	
	public void drawBonus() {
		attackBonus.setBonus(unit.getAttackAttribute().getBonusValue());
		defenceBonus.setBonus(unit.getDefenceAttribute().getBonusValue());
	}
}
