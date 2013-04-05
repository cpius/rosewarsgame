package com.wotr.strategy.action;

import java.util.Collection;

import com.wotr.model.Action;
import com.wotr.model.unit.Unit;

public interface ActionsResolverStrategy {

	Collection<Action> getActions(Unit originalunit);

}
