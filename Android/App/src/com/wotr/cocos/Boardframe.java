package com.wotr.cocos;

import org.cocos2d.types.CGPoint;

import com.wotr.model.Position;

public interface Boardframe {

	CGPoint getPosition(Position position);

	float getLaneWidth();

	Position getPositionInPerimeter(CGPoint ccp);

	CGPoint getPosition(int x, int y);

}
