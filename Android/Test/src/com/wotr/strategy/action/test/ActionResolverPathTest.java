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
import com.wotr.model.unit.basic.Archer;
import com.wotr.model.unit.basic.Ballista;
import com.wotr.model.unit.basic.LightCavalry;
import com.wotr.model.unit.basic.Pikeman;
import com.wotr.strategy.action.ActionsResolver;
import com.wotr.strategy.action.ActionsResolverStrategy;
import com.wotr.strategy.action.ZocBlockStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;
import com.wotr.strategy.factory.GameFactory;
import com.wotr.strategy.game.DefaultTurnStrategy;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.player.Player;

@RunWith(MockitoJUnitRunner.class)
public class ActionResolverPathTest {

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
		//when(gameFactory.getTurnStrategy()).thenReturn(new DefaultTurnStrategy(game));
		
		GameManager.setFactory(gameFactory);
	}

	@Test
	public void testPath() {	
		
		when(gameFactory.getTurnStrategy()).thenReturn(new DefaultTurnStrategy(game));
		
		// Attacking unites "wall"
		aUnits.put(new Position(1, 0), new LightCavalry());
		aUnits.put(new Position(1, 1), new Archer());
		aUnits.put(new Position(1, 2), new Ballista());
		aUnits.put(new Position(1, 3), new Ballista());

		// The attacking unit
		aUnits.put(new Position(0, 2), new Archer());

		// Defending units
		dUnits.put(new Position(0, 3), new Pikeman());
		dUnits.put(new Position(0, 4), new LightCavalry());

		try {
			Unit aUnit = aUnits.get(new Position(0, 2));

			ActionsResolverStrategy ac = new ActionsResolver(5, 8, game);
			Collection<Action> actions = ac.getActions(aUnit);
			
			Assert.assertEquals(3, actions.size());
			
			List<Action> list = new ArrayList<Action>();
			list.addAll(actions);
			
			Action action = list.get(0);			
			Assert.assertTrue(action instanceof MoveAction);
			Assert.assertEquals(new Position(0, 1), action.getPosition());
			Assert.assertTrue(action.getPath().getPath().isEmpty());
			
			action = list.get(1);			
			Assert.assertTrue(action instanceof AttackAction);
			Assert.assertEquals(new Position(0, 3), action.getPosition());
			//Assert.assertTrue(action.getPath().getPath().isEmpty());			

		} catch (Exception e) {
			e.printStackTrace();
			Assert.fail();
		}
	}
}
