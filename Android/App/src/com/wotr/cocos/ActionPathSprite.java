package com.wotr.cocos;

import java.util.List;

import javax.microedition.khronos.opengles.GL10;

import org.cocos2d.nodes.CCNode;
import org.cocos2d.opengl.CCDrawingPrimitives;
import org.cocos2d.types.CGPoint;

import com.wotr.model.Action;
import com.wotr.model.ActionPath;
import com.wotr.model.Position;

public class ActionPathSprite extends CCNode {

	private final Boardframe bordframe;
	private final Action action;

	public ActionPathSprite(Action action, Boardframe bordframe) {
		this.action = action;
		this.bordframe = bordframe;
	}

	@Override
	public void draw(GL10 gl) {
		gl.glDisable(GL10.GL_TEXTURE_2D);
		gl.glDisableClientState(GL10.GL_COLOR_ARRAY);
		gl.glColor4f(1.0f, 0.0f, 0.0f, 1.0f);

		gl.glDisable(GL10.GL_LINE_SMOOTH);
		gl.glLineWidth(5.0f);
		
		ActionPath path = action.getPath();
		
		//CGPoint source = bordframe.getPosition(action.getPosition());
		//CGPoint destination = bordframe.getPosition(path.getPosition());		
		
		List<Position> pathList = path.getPath();		
		CGPoint source = bordframe.getPosition(path.getPosition());
		for (Position position : pathList) {
			CGPoint destination = bordframe.getPosition(position);
			
			CCDrawingPrimitives.ccDrawLine(gl, source, destination);
			source = destination;
		}
		
		Position position = action.getUnit().getPosition();
		CGPoint destination = bordframe.getPosition(position);
		CCDrawingPrimitives.ccDrawLine(gl, source, destination);
		
		gl.glEnableClientState(GL10.GL_COLOR_ARRAY);
        gl.glEnable(GL10.GL_TEXTURE_2D);

		
	}
}
