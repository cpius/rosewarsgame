package com.wotr.strategy.action;

import java.util.Collection;

import com.wotr.model.Action;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;

public interface ActionsResolverStrategy {

	ActionCollection<Action> getActions(Unit originalunit);

	Collection<Action> getRemainingMoveActions(Unit originalunit, Position position, int pathProgress);

}
