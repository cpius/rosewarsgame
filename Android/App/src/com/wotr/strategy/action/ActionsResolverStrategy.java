package com.wotr.strategy.action;

import com.wotr.model.Action;
import com.wotr.model.unit.Unit;

public interface ActionsResolverStrategy {

	ActionCollection<Action> getActions(Unit originalunit);

}
