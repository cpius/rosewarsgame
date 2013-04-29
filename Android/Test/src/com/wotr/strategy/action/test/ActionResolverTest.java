package com.wotr.strategy.action.test;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;

import java.util.Collection;
import java.util.Map;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.Direction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.basic.Archer;
import com.wotr.model.unit.basic.Ballista;
import com.wotr.model.unit.basic.Catapult;
import com.wotr.model.unit.basic.LightCavalry;
import com.wotr.model.unit.basic.Pikeman;
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
public class ActionResolverTest {

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

		// Attacking unites
		aUnits.put(new Position(1, 6), new LightCavalry());
		aUnits.put(new Position(2, 7), new Archer());
		aUnits.put(new Position(0, 4), new Ballista());

		// Defending units
		dUnits.put(new Position(2, 5), new Pikeman());
		dUnits.put(new Position(4, 5), new LightCavalry());
		dUnits.put(new Position(1, 2), new Catapult());

		when(zbStrategy.isDirectionBlocked(any(Unit.class), any(Direction.class), any(Position.class), any(Map.class), any(Map.class))).thenReturn(false);
		ActionResolverFactory.setZocBlockStrategy(zbStrategy);

		when(attackingPlayer.getUnitMap()).thenReturn(aUnits);
		when(defendingPlayer.getUnitMap()).thenReturn(dUnits);
		when(game.getAttackingPlayer()).thenReturn(attackingPlayer);
		when(game.getDefendingPlayer()).thenReturn(defendingPlayer);
		when(gameFactory.getTurnStrategy()).thenReturn(new DefaultTurnStrategy(game));
	}

	@Test
	public void testActionResolverMelee() {

		try {
			Unit aUnit = aUnits.get(new Position(1, 6));

			ActionsResolverStrategy ac = new ActionsResolver(5, 8, game);
			ActionCollection<Action> actionCollection = ac.getActions(aUnit);
			Collection<Action> actions = actionCollection.getActions();
			
			Collection<Position> attackPositions = actionCollection.getAttackPositions();
			Collection<Position> movePositions = actionCollection.getMovePositions();
			
			Assert.assertEquals(113, actions.size());
			Assert.assertEquals(20, attackPositions.size()  + movePositions.size());

			Assert.assertTrue(movePositions.contains(new Position(0, 3)));
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

			ActionsResolverStrategy ac = new ActionsResolver(5, 8, game);
			ActionCollection<Action> actionCollection = ac.getActions(aUnit);
			Collection<Action> actions = actionCollection.getActions();

			Assert.assertEquals(0, actions.size());
		} catch (Exception e) {
			e.printStackTrace();
			Assert.fail();
		}
	}

	@Test
	public void testActionResolverRanged() {

		Unit aUnit = aUnits.get(new Position(2, 7));

		ActionsResolverStrategy ac = new ActionsResolver(5, 8, game);
		ActionCollection<Action> actionCollection = ac.getActions(aUnit);
		Collection<Action> actions = actionCollection.getActions();

		Assert.assertEquals(25, actions.size());

		Assert.assertTrue(actions.contains(new MoveAction(new Position(3, 7))));
		Assert.assertTrue(actions.contains(new MoveAction(new Position(1, 7))));
		Assert.assertTrue(actions.contains(new AttackAction(new Position(2, 5))));
		Assert.assertTrue(actions.contains(new AttackAction(new Position(4, 5))));
		Assert.assertTrue(actions.contains(new MoveAction(new Position(2, 6))));

	}
}
