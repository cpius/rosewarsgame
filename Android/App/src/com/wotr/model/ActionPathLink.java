package com.wotr.model;

import java.util.ArrayList;
import java.util.List;

public class ActionPathLink implements ActionPath {

	private final Position position;
	private final ActionPath pathToPosition;

	public ActionPathLink(Position position, ActionPath pathToPosition) {
		this.position = position;
		this.pathToPosition = pathToPosition;
	}

	@Override
	public List<Position> getPath() {

		List<Position> result = new ArrayList<Position>();

		ActionPath previousPath = getPreviousPath();
		while (previousPath != null) {
			result.add(previousPath.getPosition());
			previousPath = previousPath.getPreviousPath();
		}

		return result;
	}

	@Override
	public ActionPath getPreviousPath() {
		return pathToPosition;
	}

	@Override
	public Position getPosition() {
		return position;
	}
}
