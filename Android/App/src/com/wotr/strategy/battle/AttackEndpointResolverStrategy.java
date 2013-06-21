package com.wotr.strategy.battle;

import java.util.Collection;

import com.wotr.model.ActionPath;
import com.wotr.model.attack.AttackEndPosition;
import com.wotr.strategy.game.AttackEnder;

public interface AttackEndpointResolverStrategy {

	Collection<AttackEndPosition> getAttackEndpointPositions(AttackEnder ender, boolean succes, ActionPath actionPath);

}
