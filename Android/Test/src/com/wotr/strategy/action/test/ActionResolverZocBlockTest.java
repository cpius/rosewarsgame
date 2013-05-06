package com.wotr.strategy.action.test;

import static org.mockito.Mockito.when;

import java.util.Collection;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.wotr.GameManager;
import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.basic.HeavyCavalry;
import com.wotr.model.unit.basic.Pikeman;
import com.wotr.strategy.action.ActionCollection;
import com.wotr.strategy.action.ActionsResolver;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.action.UnitTypeZocBlockStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;
import com.wotr.strategy.factory.GameFactory;
import com.wotr.strategy.game.DefaultTurnStrategy;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.player.Player;

@RunWith(MockitoJUnitRunner.class)
public class ActionResolverZocBlockTest {

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

		when(attackingPlayer.getUnitMap()).thenReturn(aUnits);
		when(defendingPlayer.getUnitMap()).thenReturn(dUnits);
		when(game.getAttackingPlayer()).thenReturn(attackingPlayer);
		when(game.getDefendingPlayer()).thenReturn(defendingPlayer);
		when(gameFactory.getTurnStrategy()).thenReturn(new DefaultTurnStrategy(game));

		GameManager.setFactory(gameFactory);
	}

	@Test
	public void testActionResolverZocBlockFromRules() {

		Unit aUnit = aUnits.get(new Position(1, 2));
		ActionsResolverStrategy ac = new ActionsResolver(5, 4, game);
		ActionCollection<Action> actionCollection = ac.getActions(aUnit);
		Collection<Action> actions1 = actionCollection.getActions();

		aUnit = aUnits.get(new Position(3, 1));
		actionCollection = ac.getActions(aUnit);
		Collection<Action> actions2 = actionCollection.getActions();

		Assert.assertEquals(12, actions1.size());

		Assert.assertEquals(4, actions2.size());

		Assert.assertTrue(actions2.contains(new AttackAction(new Position(2, 1))));
		Assert.assertTrue(actions2.contains(new MoveAction(new Position(4, 0))));
		Assert.assertTrue(actions2.contains(new MoveAction(new Position(4, 1))));
		Assert.assertTrue(actions2.contains(new MoveAction(new Position(4, 2))));
	}
}
