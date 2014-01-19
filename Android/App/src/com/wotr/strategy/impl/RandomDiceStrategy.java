package com.wotr.strategy.impl;

import java.util.Random;

import com.wotr.strategy.DiceStrategy;

public class RandomDiceStrategy implements DiceStrategy {

	private int max;
	private Random diceRoller = new Random();

	public RandomDiceStrategy(int max) {
		this.max = max;
	}

	@Override
	public int roll() {
		return diceRoller.nextInt(max - 1) + 1;
	}
}
