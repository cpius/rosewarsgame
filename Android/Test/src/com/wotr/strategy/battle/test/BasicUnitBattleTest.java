package com.wotr.strategy.battle.test;

import junit.framework.Assert;

import org.junit.Test;

import com.wotr.GameManager;
import com.wotr.model.unit.Archer;
import com.wotr.model.unit.HeavyCavalry;
import com.wotr.model.unit.Pikeman;
import com.wotr.model.unit.Unit;
import com.wotr.strategy.DiceStrategy;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.facade.DefaultGameFactory;
import com.wotr.strategy.impl.StaticDiceStrategy;

public class BasicUnitBattleTest {

	@Test
	public void testSuccesfulArcherVSArcherAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(4, 3);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Archer();
		Unit defendingUnit = new Archer();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertTrue(success);
		Assert.assertEquals(101011, tbl.getObservations());

	}

	@Test
	public void testNonSuccesfulArcherVSArcherAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(3);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Archer();
		Unit defendingUnit = new Archer();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(101, tbl.getObservations());
	}

	@Test
	public void testDefendedArcherVSArcherAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(6, 2);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Archer();
		Unit defendingUnit = new Archer();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(11011, tbl.getObservations());
	}

	@Test
	public void testSuccesfulArcherVSHeavyCavalryAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(5, 4);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Archer();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertTrue(success);
		Assert.assertEquals(101011, tbl.getObservations());
	}

	@Test
	public void testNonSuccesfulArcherVSHeavyCavalryAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(4);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Archer();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(101, tbl.getObservations());
	}

	@Test
	public void testDefendedArcherVSHeavyCavalryAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(6, 3);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Archer();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(11011, tbl.getObservations());
	}

	@Test
	public void testSuccesfulPikemanVSHeavyCavalryAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(4, 4);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Pikeman();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertTrue(success);
		Assert.assertEquals(101011, tbl.getObservations());
	}

	@Test
	public void testNonSuccesfulPikemandVSHeavyCavalryAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(3);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Pikeman();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(101, tbl.getObservations());
	}

	@Test
	public void testDefededPikemandVSHeavyCavalryAttack() {

		BattleStrategy bs = GameManager.setFactory(new DefaultGameFactory() {
			@Override
			public DiceStrategy getDiceStrategy() {
				return new StaticDiceStrategy(4, 3);
			}
		}).getBattleStrategy();

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Pikeman();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(11011, tbl.getObservations());
	}
}
