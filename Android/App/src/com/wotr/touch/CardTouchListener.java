package com.wotr.touch;

public interface CardTouchListener {

	void cardDragedEnded(float x, float y);

	void cardMoved(float x, float y);

	void cardSelected(float x, float y);
	
	void cardDeSelected(float x, float y);	
}
