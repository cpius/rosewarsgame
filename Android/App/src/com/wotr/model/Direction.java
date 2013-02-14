package com.wotr.model;

public class Direction extends Position {

	public static final Direction[] up = { new Direction(0, -1) };
	public static final Direction[] allDirections = { new Direction(0, -1), new Direction(0, +1), new Direction(-1, 0), new Direction(1, 0) };

	public Direction(int x, int y) {
		super(x, y);
	}

	public String toString() {
		if (getX() == 0) {
			if (getY() == 1) {
				return "Down";
			} else {
				return "Up";
			}
		} else {
			if (getX() == 1) {
				return "Right";
			} else {
				return "Left";
			}
		}
	}
}
