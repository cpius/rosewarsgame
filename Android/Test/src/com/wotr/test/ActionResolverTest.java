package com.wotr.test;

import java.util.Collection;
import java.util.Map;

import org.junit.Before;
import org.junit.Test;

import com.wotr.model.Action;
import com.wotr.model.Position;
import com.wotr.model.unit.Archer;
import com.wotr.model.unit.Ballista;
import com.wotr.model.unit.Catapult;
import com.wotr.model.unit.LightCavalry;
import com.wotr.model.unit.Pikeman;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
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
	}

	@Test
	public void testActionResolverMelee() {

		Unit aUnit = aUnits.get(new Position(1, 6));

		ActionResolver ac = new ActionResolver(5, 8);
		Collection<Action> actions = ac.getActions(aUnit, aUnits, dUnits);
		
		for (Action action : actions) {
			System.out.println(action);
		}		
	}
	
	@Test
	public void testActionResolverRanged() {

		Unit aUnit = aUnits.get(new Position(2, 7));

		ActionResolver ac = new ActionResolver(5, 8);
		Collection<Action> actions = ac.getActions(aUnit, aUnits, dUnits);
		
		for (Action action : actions) {
			System.out.println(action);
		}		
	}
}
