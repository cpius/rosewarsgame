package com.wotr.model.unit;

import java.util.HashMap;

import com.wotr.model.Position;

public class UnitMap<K extends Position, V extends Unit> extends HashMap<K, V> {

	private static final long serialVersionUID = 1L;

	@Override
	public V put(K key, V value) {
		value.setPosition(key);
		return super.put(key, value);
	}

	@Override
	public V remove(Object key) {
		V result = super.remove(key);
		if(result != null) {
			result.setPosition(null);
		}
		return result;
	}

	public UnitMap<Position, Unit> getMirrored(int xRange, int yRange) {

		UnitMap<Position, Unit> result = new UnitMap<Position, Unit>();

		for (Unit unit : this.values()) {
			try {
				Unit newUnit = (Unit) unit.clone();
				newUnit.setEnemy(!unit.isEnemy());

				Position pos = mirror(xRange, yRange, unit.getPosition());
				result.put(pos, newUnit);

			} catch (CloneNotSupportedException e) {
				e.printStackTrace();
			}
		}

		return result;
	}

	private Position mirror(int xRange, int yRange, Position posistion) {

		int x = Math.abs(posistion.getX() + 1 - xRange);
		int y = Math.abs(posistion.getY() + 1 - yRange);

		return new Position(x, y);
	}
	
}
