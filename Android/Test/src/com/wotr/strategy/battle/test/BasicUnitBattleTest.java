package com.wotr.strategy.battle.test;

import static org.mockito.Mockito.when;
import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.wotr.GameManager;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.basic.Archer;
import com.wotr.model.unit.basic.HeavyCavalry;
import com.wotr.model.unit.basic.Pikeman;
import com.wotr.strategy.battle.BattleStrategy;
import com.wotr.strategy.battle.DefaultAttackStrategy;
import com.wotr.strategy.battle.DefaultBattleStrategy;
import com.wotr.strategy.battle.DefaultBonusStrategy;
import com.wotr.strategy.battle.DefaultDefenceStrategy;
import com.wotr.strategy.battle.unit.ArcherAttackStrategy;
import com.wotr.strategy.battle.unit.PikemanAttackStrategy;
import com.wotr.strategy.factory.GameFactory;
import com.wotr.strategy.impl.StaticDiceStrategy;

@RunWith(MockitoJUnitRunner.class)
public class BasicUnitBattleTest {

	@Mock
	private GameFactory gameFactory;

	@Before
	public void setUp() throws Exception {

		when(gameFactory.getBattleStrategy()).thenReturn(new DefaultBattleStrategy());

		when(gameFactory.getPikemanAttackStrategy()).thenReturn(new PikemanAttackStrategy());
		when(gameFactory.getArcherAttackStrategy()).thenReturn(new ArcherAttackStrategy());
		when(gameFactory.getAttackStrategy()).thenReturn(new DefaultAttackStrategy());
		when(gameFactory.getDefenceStrategy()).thenReturn(new DefaultDefenceStrategy());
		
		when(gameFactory.getBonusStrategy()).thenReturn(new DefaultBonusStrategy());

	}

	@Test
	public void testSuccesfulArcherVSArcherAttack() {

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(4, 3));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(3));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(6, 2));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(5, 4));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(4));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(6, 3));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(4, 4));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(3));

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

		BattleStrategy bs = GameManager.setFactory(gameFactory).getBattleStrategy();

		when(gameFactory.getDiceStrategy()).thenReturn(new StaticDiceStrategy(4, 3));

		TestBattleListener tbl = new TestBattleListener();

		bs.addBattleListener(tbl);
		Unit attackingUnit = new Pikeman();
		Unit defendingUnit = new HeavyCavalry();

		boolean success = bs.battle(attackingUnit, defendingUnit);
		Assert.assertFalse(success);
		Assert.assertEquals(11011, tbl.getObservations());
	}
}
