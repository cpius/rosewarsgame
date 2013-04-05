package com.wotr.touch;

import android.util.Log;

public class CardTouchHandler {

	private static final long BUTTON_TIME = 500;

	private long timer = 0;

	private boolean touching = false;
	private boolean selected = false;

	private CardTouchListener listener;

	private float startX;
	private float startY;

	public void addListener(CardTouchListener listener) {
		this.listener = listener;
	}

	public synchronized boolean touchStarted(float x, float y) {
		this.startX = x;
		this.startY = y;

		Log.i("Touch", "TouchStarted = " + x + ":" + y);

		if (!touching) {
			timer = System.currentTimeMillis();
			touching = true;
			return !selected;
		}
		return false;
	}

	public synchronized boolean touchEnded(float x, float y) {

		Log.v("Touch", "TouchEnded = " + x + ":" + y);

		if (touching) {
			long currentTime = System.currentTimeMillis();

			boolean hasMoved = hasMoved(x, y, startX, startY);
			if (currentTime - timer > BUTTON_TIME || hasMoved) {

				if (!selected) {
					listener.cardDragedEnded(x, y);
				}
			} else {

				if (selected) {
					listener.cardDeSelected(x, y);
				} else {
					listener.cardSelected(x, y);
				}

				selected = !selected;
			}

			touching = false;
			return true;
		}

		return false;
	}

	private boolean hasMoved(float x, float y, float startX, float startY) {
		float move = Math.abs(x - startX) + Math.abs(y - startY);
		boolean moved = move > 60;
		Log.v("Touch", "Moved = " + moved + ":" + move);
		return moved;
	}

	public void touchMoved(float x, float y) {
		if (touching && !selected) {
			listener.cardMoved(x, y);
		}
	}
}
