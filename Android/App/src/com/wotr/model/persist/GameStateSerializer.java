package com.wotr.model.persist;

public interface GameStateSerializer<IN extends GameState, OUT> {

	public IN deserialize(OUT out);

	public OUT serialize(IN in);

}
