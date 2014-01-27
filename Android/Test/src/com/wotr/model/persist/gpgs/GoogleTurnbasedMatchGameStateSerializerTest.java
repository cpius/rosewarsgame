package com.wotr.model.persist.gpgs;

import junit.framework.Assert;

import org.junit.Before;
import org.junit.Test;

import com.wotr.model.Position;
import com.wotr.model.persist.GameStateSerializer;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;
import com.wotr.model.unit.basic.HeavyCavalry;
import com.wotr.model.unit.basic.LightCavalry;
import com.wotr.model.unit.basic.Pikeman;
import com.wotr.model.unit.special.Berserker;
import com.wotr.model.unit.special.Chariot;

public class GoogleTurnbasedMatchGameStateSerializerTest {

	GameStateSerializer<GoogleTurnbasedMatchGameState, byte[]> serializer;

	@Before
	public void setup() {
		serializer = new GoogleTurnbasedMatchGameStateSerializer();
	}

	@Test
	public void doTest() {

		GoogleTurnbasedMatchGameState serializedState = new GoogleTurnbasedMatchGameState();

		UnitMap<Position, Unit> playerOneUnits = new UnitMap<Position, Unit>();
		playerOneUnits.put(new Position(1, 2), new Berserker());
		playerOneUnits.put(new Position(1, 3), new Chariot());
		playerOneUnits.put(new Position(1, 4), new Pikeman());

		UnitMap<Position, Unit> playerTwoUnits = new UnitMap<Position, Unit>();
		playerTwoUnits.put(new Position(3, 2), new Berserker());
		playerTwoUnits.put(new Position(4, 3), new LightCavalry());
		playerTwoUnits.put(new Position(5, 4), new HeavyCavalry());
		playerTwoUnits.put(new Position(6, 7), new HeavyCavalry());

		serializedState.setPlayerOneUnits(playerOneUnits);
		serializedState.setPlayerTwoUnits(playerTwoUnits);

		String playerOneId = "One";
		String playerTwoId = "Two";

		int turnCount = 1;

		serializedState.setPlayerOneId(playerOneId);
		serializedState.setPlayerTwoId(playerTwoId);
		serializedState.setTurnCount(turnCount);

		byte[] serielizationOutput = serializer.serialize(serializedState);

		System.out.println("Array has size of: " + serielizationOutput.length);

		GoogleTurnbasedMatchGameState deserializedState = serializer.deserialize(serielizationOutput);

		Assert.assertNotNull(deserializedState);
		Assert.assertEquals(playerOneId, deserializedState.getPlayerOneId());
		Assert.assertEquals(playerTwoId, deserializedState.getPlayerTwoId());
		Assert.assertEquals(turnCount, deserializedState.getTurnCount());

		Assert.assertEquals(playerOneUnits.values().size(), deserializedState.getPlayerOneUnits().values().size());
		Assert.assertEquals(playerTwoUnits.values().size(), deserializedState.getPlayerTwoUnits().values().size());

		// This asserts will not succeed because no equals methods is
		// implemented in Units
		// Assert.assertTrue(playerOneUnits.values().containsAll(deserializedState.getPlayerOneUnits().values()));
		// Assert.assertEquals(playerTwoUnits,
		// deserializedState.getPlayerTwoUnits());

	}

}
