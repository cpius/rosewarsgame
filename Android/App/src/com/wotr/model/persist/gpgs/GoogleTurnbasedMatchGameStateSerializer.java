package com.wotr.model.persist.gpgs;

import java.io.BufferedOutputStream;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;

import com.wotr.model.persist.GameStateSerializer;

public class GoogleTurnbasedMatchGameStateSerializer implements GameStateSerializer<GoogleTurnbasedMatchGameState, byte[]> {

	@Override
	public GoogleTurnbasedMatchGameState deserialize(byte[] out) {
		try {
			ByteArrayInputStream bais = new ByteArrayInputStream(out);
			ObjectInputStream in = new ObjectInputStream(bais);
			GoogleTurnbasedMatchGameState state = (GoogleTurnbasedMatchGameState) in.readObject();
			in.close();
			bais.close();
			return state;
		} catch (IOException e) {
			e.printStackTrace();
		} catch (ClassNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		return null;
	}

	@Override
	public byte[] serialize(GoogleTurnbasedMatchGameState state) {

		try {
			ByteArrayOutputStream baos = new ByteArrayOutputStream();
			OutputStream buf = new BufferedOutputStream(baos);
			ObjectOutputStream out = new ObjectOutputStream(buf);
			out.writeObject(state);
			out.close();
			buf.close();

			byte[] byteArray = baos.toByteArray();
			baos.close();

			return byteArray;

		} catch (IOException e) {

			// TODO Handle error
			e.printStackTrace();
		}

		return null;
	}

}
