package com.wotr.strategy.action.test;

import java.util.Collection;
import java.util.Map;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;

import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.Direction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Archer;
import com.wotr.model.unit.Ballista;
import com.wotr.model.unit.Catapult;
import com.wotr.model.unit.LightCavalry;
import com.wotr.model.unit.Pikeman;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.action.ZocBlockStrategy;
import com.wotr.strategy.facade.ActionResolverFactory;
import com.wotr.strategy.impl.ActionResolver;

public class ActionResolverTest {

	private Map<Position, Unit> aUnits;
	private Map<Position, Unit> dUnits;

	@Before
	public void setUp() throws Exception {

		aUnits = new UnitMap<Position, Unit>();
		dUnits = new UnitMap<Position, Unit>();

		// Attacking unites
		aUnits.put(new Position(1, 6), new LightCavalry());
		aUnits.put(new Position(2, 7), new Archer());
		aUnits.put(new Position(0, 4), new Ballista());

		// Defending units
		dUnits.put(new Position(2, 5), new Pikeman());
		dUnits.put(new Position(4, 5), new LightCavalry());
		dUnits.put(new Position(1, 2), new Catapult());
		
		ActionResolverFactory.setZocBlockStrategy(new ZocBlockStrategy() {

			@Override
			public boolean isDirectionBlocked(Unit unit, Direction d, Position pos, Map<Position, Unit> attackingUnits, Map<Position, Unit> defendingUnits) {
				return false;
			}
		});
	}

	@Test
	public void testActionResolverMelee() {

		try {
			Unit aUnit = aUnits.get(new Position(1, 6));

			ActionResolver ac = new ActionResolver(5, 8);
			Collection<Action> actions = ac.getActions(aUnit, aUnits, dUnits);

			Assert.assertEquals(20, actions.size());

			Assert.assertTrue(actions.contains(new MoveAction(new Position(0, 3))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(0, 5))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(0, 6))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(0, 7))));

			Assert.assertTrue(actions.contains(new AttackAction(new Position(1, 2))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(1, 3))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(1, 4))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(1, 5))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(1, 7))));

			Assert.assertTrue(actions.contains(new MoveAction(new Position(2, 3))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(2, 4))));
			Assert.assertTrue(actions.contains(new AttackAction(new Position(2, 5))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(2, 6))));

			Assert.assertTrue(actions.contains(new MoveAction(new Position(3, 4))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(3, 5))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(3, 6))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(3, 7))));

			Assert.assertTrue(actions.contains(new AttackAction(new Position(4, 5))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(4, 6))));
			Assert.assertTrue(actions.contains(new MoveAction(new Position(4, 7))));
		} catch (Exception e) {
			e.printStackTrace();
			Assert.fail();
		}
	}

	@Test
	public void testActionResolverMeleeBockedByFriendly() {

		try {
			aUnits.put(new Position(0, 0), new LightCavalry());
			aUnits.put(new Position(0, 1), new Archer());
			aUnits.put(new Position(1, 0), new Archer());
			
			Unit aUnit = aUnits.get(new Position(0, 0));

			ActionResolver ac = new ActionResolver(5, 8);
			Collection<Action> actions = ac.getActions(aUnit, aUnits, dUnits);

			Assert.assertEquals(0, actions.size());
		} catch (Exception e) {
			e.printStackTrace();
			Assert.fail();
		}
	}
	
	@Test
	public void testActionResolverRanged() {

		Unit aUnit = aUnits.get(new Position(2, 7));

		ActionResolver ac = new ActionResolver(5, 8);
		Collection<Action> actions = ac.getActions(aUnit, aUnits, dUnits);

		Assert.assertEquals(5, actions.size());

		Assert.assertTrue(actions.contains(new MoveAction(new Position(3, 7))));
		Assert.assertTrue(actions.contains(new MoveAction(new Position(1, 7))));
		Assert.assertTrue(actions.contains(new AttackAction(new Position(2, 5))));
		Assert.assertTrue(actions.contains(new AttackAction(new Position(4, 5))));
		Assert.assertTrue(actions.contains(new MoveAction(new Position(2, 6))));

	}
}
