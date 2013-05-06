//
//  GameTypeScene.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/17/13.
//  Copyright 2013 __MyCompanyName__. All rights reserved.
//

#import "GameTypeScene.h"
#import "ConstructDeckScene.h"
#import "GCTurnBasedMatchHelper.h"
#import "GameManager.h"
#import "GameScene.h"

@implementation GameTypeScene

+ (id)scene {
    
    CCScene *scene = [CCScene node];
    
    GameTypeScene *layer = [GameTypeScene node];
    
    [scene addChild:layer];
    
    return scene;
}

- (id)init {
    
    self = [super init];
    
    if (self) {
		// ask director for the window size
		CGSize size = [[CCDirector sharedDirector] winSize];
        
        [GCTurnBasedMatchHelper sharedInstance].delegate = self;
        
        CCLabelTTF *headline = [CCLabelTTF labelWithString:@"War Of The Roses" fontName:APP_FONT fontSize:32];
        headline.anchorPoint = ccp(0.5, 1);
        [headline setPosition:ccp(size.width / 2, size.height - 25)];
        [self addChild:headline];
		
        // Default font size will be 28 points.
		[CCMenuItemFont setFontSize:28];
        [CCMenuItemFont setFontName:APP_FONT];
		
		CCMenuItem *singlePlayerMenuItem = [CCMenuItemFont itemWithString:@"Single player" block:^(id sender) {
			         
            [[GameManager sharedManager] startNewGameOfType:kGameTypeSinglePlayer];
            
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
            [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[ConstructDeckScene scene]]];
            
		}];
        
        CCMenuItem *multiplayerMenuItem = [CCMenuItemFont itemWithString:@"Multiplayer" block:^(id sender) {
            
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
            [[GCTurnBasedMatchHelper sharedInstance] findMatchWithMinPlayers:2 maxPlayers:2 presentingViewController:[CCDirector sharedDirector]];
        }];
        
        CCMenuItem *leaderboardMenuItem = [CCMenuItemFont itemWithString:@"Leaderboard" block:^(id sender) {
            
            [[GCTurnBasedMatchHelper sharedInstance] showLeaderboardWithPresentingViewController:[CCDirector sharedDirector]];
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
        }];

        CCMenuItem *backMenuItem = [CCMenuItemFont itemWithString:@"Back" block:^(id sender) {
            
            CCLOG(@"Back");
            [[SoundManager sharedManager] playSoundEffectForGameEvent:kGameEventButtonClick];
            [[CCDirector sharedDirector] popScene];
        }];
        
		CCMenu *menu = [CCMenu menuWithItems:singlePlayerMenuItem, multiplayerMenuItem, leaderboardMenuItem, backMenuItem, nil];
		
		[menu alignItemsVerticallyWithPadding:20];
		[menu setPosition:ccp(size.width/2, size.height/2 + 25)];
		
		// Add the menu to the layer
		[self addChild:menu];
        
        CCSprite *background = [CCSprite spriteWithFile:@"Background.png"];
        background.anchorPoint = CGPointMake(0, 0);
        [self addChild:background z:-1];
        
        CCParticleSystem *flame1 = [CCParticleSystemQuad particleWithFile:@"flame.plist"];
        flame1.position = ccp(55,(size.height / 2) - 47);
        //flame1.scale = 0.40;
        [background addChild:flame1 z:10];
        
        CCParticleSystem *flame2 = [CCParticleSystemQuad particleWithFile:@"flame.plist"];
        flame2.position = ccp(27,(size.height / 2) - 105);
        // flame2.scale = 0.40;
        [background addChild:flame2 z:10];
        
        CCParticleSystem *flame3 = [CCParticleSystemQuad particleWithFile:@"flame.plist"];
        flame3.position = ccp(265,(size.height / 2) - 93);
        // flame3.scale = 0.40;
        [background addChild:flame3 z:10];
    }
    
    return self;
}

- (void)sendNotice:(NSString *)notice forMatch:(GKTurnBasedMatch *)match {
    
    [GKNotificationBanner showBannerWithTitle:@"Notice" message:notice completionHandler:^{
        
    }];
}

- (void)recieveEndGame:(GKTurnBasedMatch *)match {
    
    CCLOG(@"End game recieved for match: %@", match);
}

- (void)enterNewGame:(GKTurnBasedMatch *)match {
    
    CCLOG(@"New game found - staring constructing deck");
    
    [[GameManager sharedManager] startNewGameOfType:kGameTypeMultiPlayer];
    
    [GameManager sharedManager].currentGame.localUserId = [GCTurnBasedMatchHelper sharedInstance].localUserId;
    [GameManager sharedManager].currentGame.matchId = match.matchID;
    
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[ConstructDeckScene scene]]];
}

- (void)takeTurn:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Take turn");
    [[GameManager sharedManager] continueExistingGame];

    [GameManager sharedManager].currentGame.localUserId = [GCTurnBasedMatchHelper sharedInstance].localUserId;
    [GameManager sharedManager].currentGame.matchId = match.matchID;
    
    [[GameManager sharedManager].currentGame deserializeGameData:match.matchData forPlayerWithId:[GKLocalPlayer localPlayer].playerID allPlayers:[GCTurnBasedMatchHelper sharedInstance].currentPlayerIds onlyActions:NO onlyEnemyUnits:NO];
     
    if ([GameManager sharedManager].currentGame.state == kGameStateInitialState ||
        [GameManager sharedManager].currentGame.state == kGameStateFinishedPlacingCards) {
        [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[ConstructDeckScene scene]]];
    }
    else if ([GameManager sharedManager].currentGame.state == kGameStateGameStarted) {
        [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[GameScene scene]]];
    }
}

- (void)layoutMatch:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Other players turn");
    
    [[GameManager sharedManager] continueExistingGame];
    [[GameManager sharedManager].currentGame deserializeGameData:match.matchData forPlayerWithId:[GKLocalPlayer localPlayer].playerID allPlayers:[GCTurnBasedMatchHelper sharedInstance].currentPlayerIds onlyActions:NO onlyEnemyUnits:NO];
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[GameScene scene]]];

}
@end
