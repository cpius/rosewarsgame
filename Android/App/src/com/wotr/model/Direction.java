package com.wotr.model;

public class Direction extends Position {

	public static final Direction up = new Direction(0, -1);
	public static final Direction down = new Direction(0, 1);
	public static final Direction left = new Direction(-1, 0);
	public static final Direction right = new Direction(1, 0);

	public static final Direction[] allDirections = { up, down, left, right };
	public static final Direction[] perpendicularDirections = { up, right };
	public static final Direction[] nonDirections = {};

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

	public Direction opposite() {
		if (this.equals(up)) {
			return down;
		} else if (this.equals(down)) {
			return up;
		} else if (this.equals(left)) {
			return right;
		}
		return left;
	}

	public Position[] perpendicular(Position pos) {
		Position[] dirs = { new Position(pos.getX() + getY(), pos.getY() + getX()), new Position(pos.getX() - getY(), pos.getY() - getX()) };
		return dirs;
	}
}
