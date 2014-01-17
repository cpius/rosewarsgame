package com.wotr.gpgs;

import java.util.ArrayList;
import java.util.List;

import android.content.Intent;
import android.util.Log;

import com.google.android.gms.games.GamesClient;
import com.google.android.gms.games.multiplayer.realtime.RealTimeMessage;
import com.google.android.gms.games.multiplayer.realtime.RealTimeMessageReceivedListener;
import com.google.android.gms.games.multiplayer.realtime.Room;
import com.google.android.gms.games.multiplayer.realtime.RoomConfig;
import com.google.android.gms.games.multiplayer.realtime.RoomStatusUpdateListener;
import com.google.android.gms.games.multiplayer.realtime.RoomUpdateListener;
import com.google.example.games.basegameutils.GameHelper;

public class RoomCreator implements RoomUpdateListener, RealTimeMessageReceivedListener, RoomStatusUpdateListener {

	private Intent data;
	private GamesClient gamesClient;

	public RoomCreator(Intent data, GameHelper mHelper) {
		this.data = data;
		gamesClient = mHelper.getGamesClient();

	}

	public void createRoom() {

		ArrayList<String> invitees = data.getStringArrayListExtra(GamesClient.EXTRA_PLAYERS);
		RoomConfig.Builder roomConfigBuilder = makeBasicRoomConfigBuilder();
		roomConfigBuilder.addPlayersToInvite(invitees);

		RoomConfig roomConfig = roomConfigBuilder.build();
		gamesClient.createRoom(roomConfig);

	}

	// create a RoomConfigBuilder that's appropriate for your implementation
	private RoomConfig.Builder makeBasicRoomConfigBuilder() {
		return RoomConfig.builder(this).setMessageReceivedListener(this).setRoomStatusUpdateListener(this);
	}

	@Override
	public void onConnectedToRoom(Room arg0) {
	}

	@Override
	public void onDisconnectedFromRoom(Room arg0) {
	}

	@Override
	public void onP2PConnected(String arg0) {
	}

	@Override
	public void onP2PDisconnected(String participantId) {
	}

	@Override
	public void onPeerDeclined(Room arg0, List<String> arg1) {
	}

	@Override
	public void onPeerInvitedToRoom(Room arg0, List<String> arg1) {
	}

	@Override
	public void onPeerJoined(Room arg0, List<String> arg1) {
	}

	@Override
	public void onPeerLeft(Room arg0, List<String> arg1) {
	}

	@Override
	public void onPeersConnected(Room arg0, List<String> arg1) {
	}

	@Override
	public void onPeersDisconnected(Room arg0, List<String> arg1) {
	}

	@Override
	public void onRoomAutoMatching(Room room) {
	}

	@Override
	public void onRoomConnecting(Room room) {
	}

	@Override
	public void onRealTimeMessageReceived(RealTimeMessage message) {

		byte[] messageData = message.getMessageData();
		String messageString = new String(messageData);
		Log.i("RoomCrator", "Received message: " + messageString);

	}

	@Override
	public void onJoinedRoom(int arg0, Room arg1) {

	}

	@Override
	public void onLeftRoom(int statusCode, String roomId) {

	}

	@Override
	public void onRoomConnected(int statusCode, Room room) {

		// All players are connected
		// Start negotiation

	}

	@Override
	public void onRoomCreated(int statusCode, Room room) {

		if (statusCode == GamesClient.STATUS_OK) {

		}
	}
}
