package com.wotr.model;

import java.util.ArrayList;
import java.util.List;

public class ActionPathLink implements ActionPath {

	private final Position position;
	private final ActionPath pathToPosition;
	private List<Position> path = null;

	public ActionPathLink(Position position, ActionPath pathToPosition) {
		this.position = position;
		this.pathToPosition = pathToPosition;
	}

	@Override
	public List<Position> getPath() {

		if (path == null) {
			path = new ArrayList<Position>();

			ActionPath previousPath = getPreviousPath();
			while (previousPath != null) {
				path.add(previousPath.getPosition());
				previousPath = previousPath.getPreviousPath();
			}
		}
		return path;
	}

	@Override
	public ActionPath getPreviousPath() {
		return pathToPosition;
	}

	@Override
	public Position getPosition() {
		return position;
	}

	@Override
	public String toString() {
		return position.toString() + (pathToPosition != null ? pathToPosition : "");
	}

	@Override
	public int compareTo(ActionPath another) {
		return Integer.valueOf(getPath().size()).compareTo(Integer.valueOf(another.getPath().size()));
	}

	@Override
	public int getPathLength() {
		return getPath().size();
	}
}
