package com.wotr.strategy.action.test;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Map;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.wotr.GameManager;
import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.Direction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.basic.LightCavalry;
import com.wotr.model.unit.special.Berserker;
import com.wotr.strategy.action.ActionCollection;
import com.wotr.strategy.action.ActionsResolver;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.action.ZocBlockStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;
import com.wotr.strategy.factory.GameFactory;
import com.wotr.strategy.game.DefaultTurnStrategy;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.player.Player;

@RunWith(MockitoJUnitRunner.class)
public class BerserkerActionResolverPathTest {

	private UnitMap<Position, Unit> aUnits;
	private UnitMap<Position, Unit> dUnits;

	@Mock
	private Game game;

	@Mock
	private GameFactory gameFactory;

	@Mock
	Player attackingPlayer;

	@Mock
	Player defendingPlayer;

	@Mock
	ZocBlockStrategy zbStrategy;

	@SuppressWarnings("unchecked")
	@Before
	public void setUp() throws Exception {

		aUnits = new UnitMap<Position, Unit>();
		dUnits = new UnitMap<Position, Unit>();

		when(zbStrategy.isDirectionBlocked(any(Unit.class), any(Direction.class), any(Position.class), any(Map.class), any(Map.class))).thenReturn(false);
		ActionResolverFactory.setZocBlockStrategy(zbStrategy);

		when(attackingPlayer.getUnitMap()).thenReturn(aUnits);
		when(defendingPlayer.getUnitMap()).thenReturn(dUnits);
		when(game.getAttackingPlayer()).thenReturn(attackingPlayer);
		when(game.getDefendingPlayer()).thenReturn(defendingPlayer);
		when(gameFactory.getTurnStrategy()).thenReturn(new DefaultTurnStrategy(game));

		GameManager.setFactory(gameFactory);
	}

	@Test
	public void testPathBoundary() {

		// The attacking unit
		Unit aUnit = new Berserker();
		aUnits.put(new Position(0, 1), aUnit);

		// Defending units
		dUnits.put(new Position(0, 6), new LightCavalry());
		dUnits.put(new Position(4, 1), new LightCavalry());

		try {

			ActionsResolverStrategy ac = new ActionsResolver(5, 8, game);
			ActionCollection<Action> actionCollection = ac.getActions(aUnit);
			Collection<Action> actions = actionCollection.getActions();

			Assert.assertEquals(4, actions.size());

			List<Action> list = new ArrayList<Action>();
			list.addAll(actions);

			Action action = list.get(0);
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(0, 0), action.getPosition());

			action = list.get(1);
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(0, 2), action.getPosition());

			action = list.get(2);
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(1, 1), action.getPosition());

			action = list.get(3);
			Assert.assertTrue(action instanceof AttackAction);
			Assert.assertEquals(new Position(4, 1), action.getPosition());

		} catch (Exception e) {
			e.printStackTrace();
			Assert.fail();
		}
	}
	
	@Test
	public void testPathObstructed() {

		// The attacking unit
		Unit aUnit = new Berserker();
		aUnits.put(new Position(0, 1), aUnit);

		aUnits.put(new Position(1, 2), new LightCavalry());
		aUnits.put(new Position(2, 2), new LightCavalry());
		
		// Defending units
		dUnits.put(new Position(1, 3), new LightCavalry());

		try {

			ActionsResolverStrategy ac = new ActionsResolver(5, 8, game);
			ActionCollection<Action> actionCollection = ac.getActions(aUnit);
			Collection<Action> actions = actionCollection.getActions();

			Assert.assertEquals(4, actions.size());

			List<Action> list = new ArrayList<Action>();
			list.addAll(actions);

			Action action = list.get(0);
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(0, 0), action.getPosition());

			action = list.get(1);
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(0, 2), action.getPosition());			

			action = list.get(2);
			Assert.assertTrue(action instanceof AttackAction);
			Assert.assertEquals(new Position(1, 3), action.getPosition());
			
			action = list.get(3);
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(1, 1), action.getPosition());

		} catch (Exception e) {
			e.printStackTrace();
			Assert.fail();
		}
	}
}
