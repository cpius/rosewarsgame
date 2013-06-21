package com.wotr.strategy.battle.test;

import static org.mockito.Matchers.any;
import static org.mockito.Mockito.when;

import java.util.Map;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.wotr.GameManager;
import com.wotr.model.Direction;
import com.wotr.model.Position;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.strategy.action.ActionsResolver;
import com.wotr.strategy.action.ZocBlockStrategy;
import com.wotr.strategy.battle.DefaultAttackStrategy;
import com.wotr.strategy.battle.DefaultBattleStrategy;
import com.wotr.strategy.battle.DefaultDefenceStrategy;
import com.wotr.strategy.battle.unit.ArcherAttackStrategy;
import com.wotr.strategy.battle.unit.PikemanAttackStrategy;
import com.wotr.strategy.factory.ActionResolverFactory;
import com.wotr.strategy.factory.GameFactory;
import com.wotr.strategy.game.Game;
import com.wotr.strategy.game.GameEventListener;
import com.wotr.strategy.game.MultiplayerGame;
import com.wotr.strategy.game.TurnStrategy;
import com.wotr.strategy.player.Player;

@RunWith(MockitoJUnitRunner.class)
public class AwardAssignTest implements GameEventListener {

	private UnitMap<Position, Unit> player1Units;
	private UnitMap<Position, Unit> player2Units;

	@Mock
	private GameFactory gameFactory;

	@Mock
	private Player player1;

	@Mock
	private Player player2;

	@Mock
	private ZocBlockStrategy zbStrategy;

	@Mock
	private TurnStrategy turnStrategy;

	@Before
	public void setUp() throws Exception {

		when(gameFactory.getBattleStrategy()).thenReturn(new DefaultBattleStrategy());

		when(gameFactory.getPikemanAttackStrategy()).thenReturn(new PikemanAttackStrategy());
		when(gameFactory.getArcherAttackStrategy()).thenReturn(new ArcherAttackStrategy());
		when(gameFactory.getAttackStrategy()).thenReturn(new DefaultAttackStrategy());
		when(gameFactory.getDefenceStrategy()).thenReturn(new DefaultDefenceStrategy());
		
		when(gameFactory.getTurnStrategy()).thenReturn(turnStrategy);
		
		//when(turnStrategy.).thenReturn();
		
		
		player1Units = new UnitMap<Position, Unit>();
		player2Units = new UnitMap<Position, Unit>();

		when(zbStrategy.isDirectionBlocked(any(Unit.class), any(Direction.class), any(Position.class), any(Map.class), any(Map.class))).thenReturn(false);
		ActionResolverFactory.setZocBlockStrategy(zbStrategy);

		when(player1.getUnitMap()).thenReturn(player1Units);
		when(player2.getUnitMap()).thenReturn(player2Units);

		Game game = new MultiplayerGame(player1, player2);
		game.addGameEventListener(this);
		GameManager.setGame(game);
		GameManager.getFactory().getBattleStrategy().addBattleListener(new TestBattleListener());

		ActionsResolver actionsResolver = new ActionsResolver(1, 10, game);
		game.setActionsResolver(actionsResolver);

		game.startGame();

	}

	@Test
	public void testSuccesfulArcherVSArcherAttack() {

	}

	@Override
	public void gameStarted() {

	}

	@Override
	public void gameEnded(Player winner) {

	}

	@Override
	public void startTurn(Player player, int remainingActions) {

	}

	@Override
	public void actionPerformed(Player player, int remainingActions) {
	}

}
