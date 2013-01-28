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
        
        CCLabelTTF *headline = [CCLabelTTF labelWithString:@"War Of The Roses" fontName:@"AppleGothic" fontSize:32];
        headline.anchorPoint = ccp(0.5, 1);
        [headline setPosition:ccp(size.width / 2, size.height - 25)];
        [self addChild:headline];
		
        // Default font size will be 28 points.
		[CCMenuItemFont setFontSize:28];
        [CCMenuItemFont setFontName:@"AppleGothic"];
		
		CCMenuItem *singlePlayerMenuItem = [CCMenuItemFont itemWithString:@"Single player" block:^(id sender) {
			         
            [[GameManager sharedManager] startNewGameOfType:kGameTypeSinglePlayer];
            
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
            [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[ConstructDeckScene scene]]];
            
		}];
        
        CCMenuItem *multiplayerMenuItem = [CCMenuItemFont itemWithString:@"Multiplayer" block:^(id sender) {

            [[GameManager sharedManager] startNewGameOfType:kGameTypeMultiPlayer];
            
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
            
            [[GCTurnBasedMatchHelper sharedInstance] findMatchWithMinPlayers:2 maxPlayers:2 presentingViewController:[CCDirector sharedDirector]];
        }];
        
        CCMenuItem *leaderboardMenuItem = [CCMenuItemFont itemWithString:@"Leaderboard" block:^(id sender) {
            
            [[GCTurnBasedMatchHelper sharedInstance] showLeaderboardWithPresentingViewController:[CCDirector sharedDirector]];
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
        }];

        CCMenuItem *backMenuItem = [CCMenuItemFont itemWithString:@"Back" block:^(id sender) {
            
            CCLOG(@"Back");
            [[SimpleAudioEngine sharedEngine] playEffect:BUTTON_CLICK_SOUND];
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
    }
    
    return self;
}

- (void)sendNotice:(NSString *)notice forMatch:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Send notice: %@ for match: %@", notice, match);
}

- (void)recieveEndGame:(GKTurnBasedMatch *)match {
    
    CCLOG(@"End game recieved for match: %@", match);
}

- (void)enterNewGame:(GKTurnBasedMatch *)match {
    
    CCLOG(@"New game found - staring constructing deck");
    
    [[CCDirector sharedDirector] replaceScene:[CCTransitionCrossFade transitionWithDuration:0.2 scene:[ConstructDeckScene scene]]];
}

- (void)takeTurn:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Take turn");
}

- (void)layoutMatch:(GKTurnBasedMatch *)match {
    
    CCLOG(@"Other players turn");
}
@end
