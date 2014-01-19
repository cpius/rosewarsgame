package com.wotr.strategy.action;

import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;

import com.wotr.model.Action;
import com.wotr.model.AttackAction;
import com.wotr.model.MoveAction;
import com.wotr.model.Position;

public class ActionCollection<T> {

	private final Collection<Action> actions;

	private Map<Position, Collection<MoveAction>> moveMap = new HashMap<Position, Collection<MoveAction>>();
	private Map<Position, Collection<AttackAction>> attackMap = new HashMap<Position, Collection<AttackAction>>();

	public ActionCollection(Collection<Action> actions) {
		this.actions = actions;

		for (Action action : actions) {

			if (action instanceof AttackAction) {
				AttackAction attackAction = (AttackAction) action;

				Collection<AttackAction> collection = attackMap.get(attackAction.getPosition());
				if (collection == null) {
					collection = new ArrayList<AttackAction>();
					attackMap.put(attackAction.getPosition(), collection);
				}
				collection.add(attackAction);

			} else if (action instanceof MoveAction) {
				MoveAction moveAction = (MoveAction) action;

				Collection<MoveAction> collection = moveMap.get(moveAction.getPosition());
				if (collection == null) {
					collection = new ArrayList<MoveAction>();
					moveMap.put(moveAction.getPosition(), collection);
				}
				collection.add(moveAction);
			}
		}
	}

	public Collection<Action> getActions() {
		return actions;
	}

	public Collection<Position> getAttackPositions() {
		return attackMap.keySet();
	}

	public Collection<Position> getMovePositions() {
		return moveMap.keySet();
	}

	public Collection<? extends Action> getActionForPosition(Position position) {
		Collection<MoveAction> result = moveMap.get(position);
		return result != null ? result : attackMap.get(position);
	}

}
