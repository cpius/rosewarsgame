package com.wotr.strategy.battle.test;

import static org.mockito.Mockito.when;

import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.runners.MockitoJUnitRunner;

import com.wotr.strategy.battle.DefaultAttackStrategy;
import com.wotr.strategy.battle.DefaultBattleStrategy;
import com.wotr.strategy.battle.DefaultDefenceStrategy;
import com.wotr.strategy.battle.unit.ArcherAttackStrategy;
import com.wotr.strategy.battle.unit.PikemanAttackStrategy;
import com.wotr.strategy.factory.GameFactory;

@RunWith(MockitoJUnitRunner.class)
public class EndPositionTest {

	@Mock
	private GameFactory gameFactory;

	@Before
	public void setUp() throws Exception {

		when(gameFactory.getBattleStrategy()).thenReturn(new DefaultBattleStrategy());

		when(gameFactory.getPikemanAttackStrategy()).thenReturn(new PikemanAttackStrategy());
		when(gameFactory.getArcherAttackStrategy()).thenReturn(new ArcherAttackStrategy());
		when(gameFactory.getAttackStrategy()).thenReturn(new DefaultAttackStrategy());
		when(gameFactory.getDefenceStrategy()).thenReturn(new DefaultDefenceStrategy());
		
		//Game game = new MultiplayerGame(playerOne, playerTwo);
		//game.addGameEventListener(this);
		//GameManager.setGame(game);
		//GameManager.getFactory().getBattleStrategy().addBattleListener(this);

		/*ActionsResolver actionsResolver = new ActionsResolver(xCount, yCount, game);
		game.setActionsResolver(actionsResolver);

		game.startGame();*/
	}

	@Test
	public void testSuccesfulArcherVSArcherAttack() {

		
	}

	
}
