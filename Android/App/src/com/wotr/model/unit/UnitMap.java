package com.wotr.model.unit;

import java.util.HashMap;

import com.wotr.model.Position;

public class UnitMap<K extends Position, V extends Unit> extends HashMap<K, V> {

	private static final long serialVersionUID = 1L;

	@Override
	public V put(K key, V value) {
		value.setPosistion(key);
		return super.put(key, value);
	}

	@Override
	public V remove(Object key) {
		V result = super.remove(key);
		result.setPosistion(null);
		return result;
	}

}
