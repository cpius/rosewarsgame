package com.wotr.model;

import java.util.List;

public interface ActionPath extends Comparable<ActionPath> {	
	
	public ActionPath getPreviousPath();
	
	public List<Position> getPath();

	public Position getPosition();
	
	public int getPathLength();

}
