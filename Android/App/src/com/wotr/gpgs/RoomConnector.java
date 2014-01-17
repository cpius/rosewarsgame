package com.wotr.gpgs;

import java.util.List;

import com.google.android.gms.games.GamesClient;
import com.google.android.gms.games.multiplayer.realtime.RealTimeMessage;
import com.google.android.gms.games.multiplayer.realtime.RealTimeMessageReceivedListener;
import com.google.android.gms.games.multiplayer.realtime.Room;
import com.google.android.gms.games.multiplayer.realtime.RoomConfig;
import com.google.android.gms.games.multiplayer.realtime.RoomStatusUpdateListener;
import com.google.android.gms.games.multiplayer.realtime.RoomUpdateListener;
import com.google.example.games.basegameutils.GameHelper;

public class RoomConnector implements RoomUpdateListener, RealTimeMessageReceivedListener, RoomStatusUpdateListener {

	private GameHelper mHelper;
	private GamesClient gamesClient;
	private Room room;
	private Room connectedRoom;

	public RoomConnector(GameHelper mHelper) {
		this.mHelper = mHelper;
		gamesClient = mHelper.getGamesClient();
	}

	public boolean connect() {

		GamesClient gamesClient = mHelper.getGamesClient();

		String invitationId = mHelper.getInvitationId();

		if (invitationId != null) {
			RoomConfig.Builder roomConfigBuilder = makeBasicRoomConfigBuilder();
			roomConfigBuilder.setInvitationIdToAccept(invitationId);
			gamesClient.joinRoom(roomConfigBuilder.build());

			return true;
		}

		return false;
	}

	private RoomConfig.Builder makeBasicRoomConfigBuilder() {
		return RoomConfig.builder(this).setMessageReceivedListener(this).setRoomStatusUpdateListener(this);
	}

	@Override
	public void onConnectedToRoom(Room room) {

	}

	@Override
	public void onDisconnectedFromRoom(Room room) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onP2PConnected(String participantId) {

	}

	@Override
	public void onP2PDisconnected(String participantId) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onPeerDeclined(Room arg0, List<String> arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onPeerInvitedToRoom(Room arg0, List<String> arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onPeerJoined(Room arg0, List<String> arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onPeerLeft(Room arg0, List<String> arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onPeersConnected(Room arg0, List<String> participantIds) {
		String name = mHelper.getPlusClient().getAccountName();

		String message = "Hey there game initiator. " + name;
		byte[] messageData = message.getBytes();

		for (String participantId : participantIds) {
			gamesClient.sendReliableRealTimeMessage(null, messageData, connectedRoom.getRoomId(), participantId);
		}
	}

	@Override
	public void onPeersDisconnected(Room arg0, List<String> arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onRoomAutoMatching(Room room) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onRoomConnecting(Room room) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onRealTimeMessageReceived(RealTimeMessage arg0) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onJoinedRoom(int arg0, Room arg1) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onLeftRoom(int statusCode, String roomId) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onRoomConnected(int statusCode, Room room) {
		// TODO Auto-generated method stub

	}

	@Override
	public void onRoomCreated(int statusCode, Room room) {
		// TODO Auto-generated method stub

	}
}
