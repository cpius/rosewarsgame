package com.wotr.model.unit;

import java.util.ArrayList;
import java.util.Collection;
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
		if (result != null) {
			result.setPosition(null);
		}
		return result;
	}

	/*
	 * public UnitMap<Position, Unit> cloneToMirror(int xRange, int yRange) {
	 * 
	 * UnitMap<Position, Unit> result = new UnitMap<Position, Unit>();
	 * 
	 * for (Unit unit : this.values()) { try { Unit newUnit = (Unit)
	 * unit.clone(); newUnit.setEnemy(!unit.isEnemy());
	 * 
	 * Position pos = mirror(xRange, yRange, unit.getPosition());
	 * result.put(pos, newUnit);
	 * 
	 * } catch (CloneNotSupportedException e) { e.printStackTrace(); } }
	 * 
	 * return result; }
	 */

	public void mirrorUnits(int xRange, int yRange) {

		UnitMap<K, V> result = new UnitMap<K, V>();
		for (V unit : this.values()) {
			@SuppressWarnings("unchecked")
			K position = (K) unit.getPosition();
			result.put(mirror(xRange, yRange, position), unit);
		}

		clear();
		putAll(result);
	}

	@SuppressWarnings("unchecked")
	private K mirror(int xRange, int yRange, K position) {

		int x = Math.abs(position.getX() + 1 - xRange);
		int y = Math.abs(position.getY() + 1 - yRange);

		return (K) new Position(x, y);
	}

	private void writeObject(java.io.ObjectOutputStream stream) throws java.io.IOException {
		ArrayList<Unit> col = new ArrayList<Unit>(this.values());
		stream.writeObject(col);
	}

	private void readObject(java.io.ObjectInputStream stream) throws java.io.IOException, ClassNotFoundException {
		@SuppressWarnings("unchecked")
		Collection<Unit> read = (ArrayList<Unit>) stream.readObject();
		for (Unit unit : read) {

			@SuppressWarnings("unchecked")
			K pos = (K) unit.getPosition();
			@SuppressWarnings("unchecked")
			V vUnit = (V) unit;
			put(pos, vUnit);
		}

	}

}
