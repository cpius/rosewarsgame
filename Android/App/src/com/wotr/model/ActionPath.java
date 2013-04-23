package com.wotr.model;

import java.util.List;

public interface ActionPath {	
	
	public ActionPath getPreviousPath();
	
	public List<Position> getPath();

	public Position getPosition();

}
