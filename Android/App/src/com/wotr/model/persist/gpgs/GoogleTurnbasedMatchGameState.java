package com.wotr.model.persist.gpgs;

import java.io.Serializable;

import com.wotr.model.Position;
import com.wotr.model.persist.GameState;
import com.wotr.model.unit.Unit;
import com.wotr.model.unit.UnitMap;

public class GoogleTurnbasedMatchGameState implements GameState, Serializable {

	private static final long serialVersionUID = 1L;

	private UnitMap<Position, Unit> playerOneUnits;
	private UnitMap<Position, Unit> playerTwoUnits;
	private String playerOneId;
	private String playerTwoId;
	private boolean playerOneSetup;
	private boolean playerTwoSetup;
	private int remainingActions;

	public UnitMap<Position, Unit> getPlayerOneUnits() {
		return playerOneUnits;
	}

	public UnitMap<Position, Unit> getPlayerTwoUnits() {
		return playerTwoUnits;
	}

	public String getPlayerOneId() {
		return playerOneId;
	}

	public String getPlayerTwoId() {
		return playerTwoId;
	}

	public void setPlayerOneUnits(UnitMap<Position, Unit> playerOneUnits) {
		this.playerOneUnits = playerOneUnits;
	}

	public void setPlayerTwoUnits(UnitMap<Position, Unit> playerTwoUnits) {
		this.playerTwoUnits = playerTwoUnits;
	}

	public void setPlayerOneId(String playerOneId) {
		this.playerOneId = playerOneId;
	}

	public void setPlayerTwoId(String playerTwoId) {
		this.playerTwoId = playerTwoId;

	}

	public void setRemainingActions(int remainingActions) {
		this.remainingActions = remainingActions;
	}
	
	public int getRemainingActions() {
		return remainingActions;
	}

	public boolean isPlayerOneSetup() {
		return playerOneSetup;
	}

	public void setPlayerOneSetup(boolean playerOneSetup) {
		this.playerOneSetup = playerOneSetup;
	}

	public boolean isPlayerTwoSetup() {
		return playerTwoSetup;
	}

	public void setPlayerTwoSetup(boolean playerTwoSetup) {
		this.playerTwoSetup = playerTwoSetup;
	}

	public boolean isSetup(String playerId) {
		if (playerId.equals(playerOneId)) {
			return playerOneSetup;
		} else if (playerId.equals(playerTwoId)) {
			return playerTwoSetup;
		}

		return false;
	}
}
