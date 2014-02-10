package com.wotr.cocos.layout.perspective;

import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGRect;

import com.wotr.cocos.Boardframe;
import com.wotr.model.Position;

public class BoardframePerspective implements Boardframe {

	private final float xOffset;
	private final float yOffset;
	private final float yMove;	

	private CGPoint[][] positions;
	private CGRect[][] perimeters;
	private final int xCount;
	private final int yCount;

	private float xCenterOffset = 0;
	private float xPerimeterSize;
	private float yPerimeterSize;

	public BoardframePerspective(int xCount, int yCount, float frameWidth, float frameHeight, float margen, float scale, float perimeterScale) {
		this.xCount = xCount;
		this.yCount = yCount;		

		float boardScale = frameHeight / frameWidth;

		float x = xCount;
		float y = scale * yCount;

		float cardSumScale = y / x;

		boolean xPrimary = boardScale > cardSumScale;
		if (xPrimary) {
			xOffset = (frameWidth - (2f * margen)) / (xCount);
			yOffset = xOffset * scale;
		} else {
			yOffset = (frameHeight - (2f * margen)) / (yCount);
			xOffset = yOffset / scale;
			xCenterOffset = frameWidth - (yOffset * yCount) / 2;
		}

		xPerimeterSize = xOffset * perimeterScale;
		yPerimeterSize = yOffset * perimeterScale;

		yMove = frameHeight - (yOffset * yCount);

		positions = new CGPoint[xCount][yCount];
		perimeters = new CGRect[xCount][yCount];
	}

	public CGPoint getPosition(int x, int y) {
		if (positions[x][y] == null) {
			float xPos = (((float) (x + 1)) * (float) xOffset) - xOffset / 2 + xCenterOffset;
			float yPos = (((float) (y + 1)) * (float) yOffset) - yOffset / 2;
			positions[x][y] = CGPoint.ccp(xPos, yPos + yMove);
		}
		return positions[x][y];
	}
	
	public CGPoint getPosition(Position position) {
		return getPosition(position.getX(), position.getY());		
	}

	public CGRect getPerimeter(int x, int y) {
		if (perimeters[x][y] == null) {

			CGPoint position = getPosition(x, y);

			float rectX = position.x - xPerimeterSize / 2;
			float recty = position.y - yPerimeterSize / 2;

			perimeters[x][y] = CGRect.make(rectX, recty, xPerimeterSize, yPerimeterSize);
		}
		return perimeters[x][y];
	}

	public Position getPositionInPerimeter(CGPoint point) {

		for (int x = 0; x < xCount; x++) {
			for (int y = 0; y < yCount; y++) {

				CGRect perimeter = getPerimeter(x, y);
				if (CGRect.containsPoint(perimeter, point)) {
					return new Position(x, y);
				}
			}
		}
		return null;
	}

	public float getLaneWidth() {
		return xOffset;
	}	
}
