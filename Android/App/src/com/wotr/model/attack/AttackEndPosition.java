package com.wotr.model.attack;

import com.wotr.model.AttackResult;
import com.wotr.model.Position;

public interface AttackEndPosition {

	public Position getPosition();

	public void endAttack();

	public void setAttackResult(AttackResult attackResult);

	public AttackResult getAttackResult();
}
