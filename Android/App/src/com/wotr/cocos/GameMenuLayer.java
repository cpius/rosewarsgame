package com.wotr.cocos;

import org.cocos2d.layers.CCLayer;
import org.cocos2d.menus.CCMenu;
import org.cocos2d.menus.CCMenuItem;
import org.cocos2d.menus.CCMenuItemFont;
import org.cocos2d.menus.CCMenuItemImage;
import org.cocos2d.nodes.CCDirector;
import org.cocos2d.nodes.CCLabel;
import org.cocos2d.nodes.CCSprite;
import org.cocos2d.types.CGPoint;
import org.cocos2d.types.CGSize;

import com.google.example.games.basegameutils.GameHelper;
import com.wotr.GameMenuListener;

public class GameMenuLayer extends CCLayer {

	private GameMenuListener listener;
	private CCMenuItem loginButton;
	private CCMenuItem logoutButton;
	private CCMenuItem multiPlayerLocalMenuItem;
	private CCMenuItem multiPlayerOnlineMenuItem;
	private CCMenuItem leaderBoardMenuItem;
	private CCMenuItem achievementsMenuItem;
	private GameHelper mHelper;

	public GameMenuLayer(GameMenuListener listener, GameHelper mHelper) {

		this.listener = listener;
		this.mHelper = mHelper;
		setIsTouchEnabled(true);

		CGSize size = CCDirector.sharedDirector().displaySize();

		CCSprite back = new CCSprite("Background-hd.png");

		back.setPosition(size.getWidth() / 2, size.getHeight() / 2);
		addChild(back);

		CCLabel headLine = CCLabel.makeLabel("War Of The Roses", "Arial", 32f);
		headLine.setAnchorPoint(CGPoint.ccp(0.5f, 1));
		headLine.setPosition(CGPoint.ccp(size.width / 2f, size.height - 25f));
		addChild(headLine);

		CCMenuItemFont.setFontSize(28);
		CCMenuItemFont.setFontName("Arial");

		CCMenuItem singlePlayerMenuItem = CCMenuItemFont.item("Single player", this, "single");
		multiPlayerLocalMenuItem = CCMenuItemFont.item("Multiplayer - Local", this, "multiPlayeLocal");
		multiPlayerOnlineMenuItem = CCMenuItemFont.item("Multiplayer - Online", this, "multiplayerOnline");
		leaderBoardMenuItem = CCMenuItemFont.item("Leaderboard", this, "showLeaderboard");
		achievementsMenuItem = CCMenuItemFont.item("Achivements", this, "showAchievements");

		multiPlayerOnlineMenuItem.setIsEnabled(false);
		leaderBoardMenuItem.setIsEnabled(false);
		achievementsMenuItem.setIsEnabled(false);

		CCMenu menu = CCMenu.menu(singlePlayerMenuItem, multiPlayerLocalMenuItem, multiPlayerOnlineMenuItem, leaderBoardMenuItem, achievementsMenuItem);

		menu.alignItemsVertically(20f);
		menu.setPosition(size.width / 2f, size.height / 2f + 25f);

		// Add the menu to the layer
		addChild(menu);

		loginButton = CCMenuItemImage.item("google/Red-signin_Long_base_20dp.png", "google/Red-signin_Long_press_20dp.png", this, "doLogin");
		loginButton.setIsEnabled(true);
		loginButton.setVisible(true);
		loginButton.setAnchorPoint(CGPoint.ccp(0.5f, 0));
		CCMenu loginMenu = CCMenu.menu(loginButton);
		loginMenu.setPosition(size.getWidth() / 2f, 10f);
		addChild(loginMenu);

		logoutButton = CCMenuItemFont.item("Logout", this, "doLogout");
		logoutButton.setIsEnabled(false);
		logoutButton.setVisible(false);
		logoutButton.setAnchorPoint(CGPoint.ccp(0.5f, 0));
		CCMenu logoutMenu = CCMenu.menu(logoutButton);
		logoutMenu.setPosition(size.getWidth() / 2f, 10f);
		addChild(logoutMenu);

		/*
		 * CCParticleSystem flame1 = new
		 * CCQuadParticleSystem("particle/flame.plist");
		 * flame1.setPosition(CGPoint.ccp(55, (size.height / 2f) - 47f));
		 * addChild(flame1);
		 * 
		 * CCParticleSystem flame2 = new
		 * CCQuadParticleSystem("particle/flame.plist");
		 * flame2.setPosition(CGPoint.ccp(27f, (size.height / 2f) - 105f));
		 * addChild(flame2);
		 * 
		 * CCParticleSystem flame3 = new
		 * CCQuadParticleSystem("particle/flame.plist");
		 * flame3.setPosition(CGPoint.ccp(265f, (size.height / 2f) - 93f));
		 * addChild(flame3);
		 */

		back.getTextureRect();
	}

	public void enableLogin(boolean enable) {
		loginButton.setIsEnabled(enable);
		loginButton.setVisible(enable);

		logoutButton.setIsEnabled(!enable);
		logoutButton.setVisible(!enable);

		multiPlayerOnlineMenuItem.setIsEnabled(!enable);
		leaderBoardMenuItem.setIsEnabled(!enable);
		achievementsMenuItem.setIsEnabled(!enable);
	}

	public void single(Object source) {
		System.out.println("single");
	}

	public void multiPlayeLocal(Object source) {
		listener.onMultiplayerLocalClicked();		
	}

	public void multiplayerOnline(Object source) {
		listener.onMultiplayerOnlineClicked();
	}

	public void showLeaderboard(Object source) {
		listener.onLeaderboardButtonClicked();
	}

	public void showAchievements(Object source) {
		listener.onAchievementsClicked();
	}

	public void doLogin(Object source) {
		listener.onSignInButtonClicked();
	}

	public void doLogout(Object source) {
		listener.onSignOutButtonClicked();
	}

}