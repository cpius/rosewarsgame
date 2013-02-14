package com.wotr.strategy.impl;

import com.wotr.strategy.DiceStrategy;

public class StaticDiceStrategy implements DiceStrategy {

	private final int[] value;
	private int count = 0;

	public StaticDiceStrategy(int... value) {
		this.value = value;
	}

	@Override
	public int roll() {
		return value[count++];
	}
}
