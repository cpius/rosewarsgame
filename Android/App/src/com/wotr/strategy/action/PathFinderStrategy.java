package com.wotr.strategy.action;

import com.wotr.model.Action;
import com.wotr.model.Position;

public interface PathFinderStrategy {

	void touch(Position position);

	Action getActionForPosition(Position position);

}
