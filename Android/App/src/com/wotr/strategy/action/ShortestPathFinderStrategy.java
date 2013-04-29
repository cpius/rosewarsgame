package com.wotr.strategy.action;

import java.util.Collection;

import com.wotr.model.Action;
import com.wotr.model.Position;

public class ShortestPathFinderStrategy implements PathFinderStrategy {

	private final ActionCollection<Action> actionCollection;

	public ShortestPathFinderStrategy(ActionCollection<Action> actionCollection) {
		this.actionCollection = actionCollection;
	}

	@Override
	public void touch(Position position) {

	}

	@Override
	public Action getActionForPosition(Position position) {
		Collection<? extends Action> actions = actionCollection.getActionForPosition(position);

		if (actions == null) {
			return null;
		}

		Action result = null;

		for (Action action : actions) {
			
			if (result == null || action.getPath().compareTo(result.getPath()) < 0 ) {
				result = action;
			}
		}

		return result;
	}

}
