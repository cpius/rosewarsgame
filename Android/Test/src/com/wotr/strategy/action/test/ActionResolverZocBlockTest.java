package com.wotr.strategy.action.test;

import java.util.Collection;
import java.util.Map;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;

import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.HeavyCavalry;
import com.wotr.model.unit.Pikeman;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.action.UnitTypeZocBlockStrategy;
import com.wotr.strategy.facade.ActionResolverFactory;
import com.wotr.strategy.impl.ActionResolver;

public class ActionResolverZocBlockTest {

	private Map<Position, Unit> aUnits;
	private Map<Position, Unit> dUnits;

	@Before
	public void setUp() throws Exception {

		aUnits = new UnitMap<Position, Unit>();
		dUnits = new UnitMap<Position, Unit>();

		// Attacking unites
		aUnits.put(new Position(1, 2), new HeavyCavalry());
		aUnits.put(new Position(3, 1), new HeavyCavalry());

		// Defending units
		dUnits.put(new Position(2, 1), new Pikeman());

		ActionResolverFactory.setZocBlockStrategy(new UnitTypeZocBlockStrategy());
	}

	@Test
	public void testActionResolverZocBlockFromRules() {

		Unit aUnit = aUnits.get(new Position(1, 2));
		ActionResolver ac = new ActionResolver(5, 4);
		Collection<Action> actions1 = ac.getActions(aUnit, aUnits, dUnits);

		aUnit = aUnits.get(new Position(3, 1));
		Collection<Action> actions2 = ac.getActions(aUnit, aUnits, dUnits);

		Assert.assertEquals(8, actions1.size());

		Assert.assertEquals(4, actions2.size());

		Assert.assertTrue(actions2.contains(new AttackAction(new Position(2, 1))));
		Assert.assertTrue(actions2.contains(new MoveAction(new Position(4, 0))));
		Assert.assertTrue(actions2.contains(new MoveAction(new Position(4, 1))));
		Assert.assertTrue(actions2.contains(new MoveAction(new Position(4, 2))));
	}
}
