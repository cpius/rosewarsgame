//
//  HKGameTypeScene.m
//  RoseWars
//
//  Created by Heine Skov Kristensen on 8/16/13.
//  Copyright (c) 2013 Heine Skov Kristensen. All rights reserved.
//

#import "HKGameTypeScene.h"
#import "HKMainMenuScene.h"
#import "HKImageButton.h"
#import "HKConstructDeckScene.h"
#import "GameManager.h"
#import "GCTurnBasedMatchHelper.h"
#import "HKGameScene.h"

@implementation HKGameTypeScene

- (void)didMoveToView:(SKView *)view {
    
    [GCTurnBasedMatchHelper sharedInstance].delegate = self;

    SKSpriteNode *backgroundNode = [SKSpriteNode spriteNodeWithImageNamed:@"Background"];
    
    backgroundNode.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMidY(self.frame));
    [self addChild:backgroundNode];
    
    SKLabelNode *headline = [SKLabelNode labelNodeWithFontNamed:APP_FONT];
    
    headline.text = @"The Rose Wars";
    headline.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetHeight(self.frame) - 50);
    headline.fontSize = 32;
    
    [self addChild:headline];
    
    HKImageButton *singlePlayerButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Single player" block:^(id sender) {
        [[GameManager sharedManager] startNewGameOfType:kGameTypeSinglePlayer];
        HKConstructDeckScene *scene = [HKConstructDeckScene sceneWithSize:self.size];
        scene.scaleMode = SKSceneScaleModeAspectFill;
        
        [view presentScene:scene transition:[SKTransition fadeWithDuration:0.5]];
    }];
    
    HKImageButton *multiPlayerButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Multiplayer" block:^(id sender) {
        [[GCTurnBasedMatchHelper sharedInstance] findMatchWithMinPlayers:2 maxPlayers:2 presentingViewController:self.view.window.rootViewController];
    }];
    
    HKImageButton *leaderboardButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Leaderboard" block:^(id sender) {
        [[GCTurnBasedMatchHelper sharedInstance] showLeaderboardWithPresentingViewController:self.view.window.rootViewController];
    }];
    
    HKImageButton *backButton = [HKImageButton imageButtonWithImage:@"button" selectedImage:@"button_selected" title:@"Back" block:^(id sender) {
        HKMainMenuScene *mainmenuScene = [HKMainMenuScene sceneWithSize:self.size];
        mainmenuScene.scaleMode = SKSceneScaleModeAspectFill;
        [view presentScene:mainmenuScene transition:[SKTransition fadeWithDuration:0.5]];
    }];
    

    [singlePlayerButton setScale:1.4];
    [multiPlayerButton setScale:1.4];
    [leaderboardButton setScale:1.4];
    [backButton setScale:1.4];
    
    singlePlayerButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetHeight(self.frame) - 150);
    multiPlayerButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(singlePlayerButton.frame) - 40);
    leaderboardButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(multiPlayerButton.frame) - 40);
    backButton.position = CGPointMake(CGRectGetMidX(self.frame), CGRectGetMinY(leaderboardButton.frame) - 40);

    [self addChild:singlePlayerButton];
    [self addChild:multiPlayerButton];
    [self addChild:leaderboardButton];
    [self addChild:backButton];
    
    SKEmitterNode *fireNode = [self newFireEmitter];
    fireNode.position = CGPointMake(55, CGRectGetHeight(self.frame) / 2 - 47);
    fireNode.xScale = 0.5;
    fireNode.yScale = 0.5;
    [self addChild:fireNode];
}

- (SKEmitterNode*)newFireEmitter {
    
    NSString *fireEmitterPath = [[NSBundle mainBundle] pathForResource:@"Flame" ofType:@"sks"];
    
    return [NSKeyedUnarchiver unarchiveObjectWithFile:fireEmitterPath];
}

- (void)sendNotice:(NSString *)notice forMatch:(GKTurnBasedMatch *)match {
    
    [GKNotificationBanner showBannerWithTitle:@"Notice" message:notice completionHandler:^{
        
    }];
}

- (void)recieveEndGame:(GKTurnBasedMatch *)match {
    
    NSLog(@"End game recieved for match: %@", match);
}

- (void)enterNewGame:(GKTurnBasedMatch *)match {
    
    NSLog(@"New game found - staring constructing deck");
    
    [[GameManager sharedManager] startNewGameOfType:kGameTypeMultiPlayer];
    
    [GameManager sharedManager].currentGame.localUserId = [GCTurnBasedMatchHelper sharedInstance].localUserId;
    [GameManager sharedManager].currentGame.matchId = match.matchID;
    
    [self.view presentScene:[HKConstructDeckScene sceneWithSize:self.size] transition:[SKTransition crossFadeWithDuration:0.5]];
}

- (void)takeTurn:(GKTurnBasedMatch *)match {
    
    NSLog(@"Take turn");
    
    [[GameManager sharedManager] continueExistingGame];
    
    [GameManager sharedManager].currentGame.localUserId = [GCTurnBasedMatchHelper sharedInstance].localUserId;
    [GameManager sharedManager].currentGame.matchId = match.matchID;
    
    [[GameManager sharedManager].currentGame deserializeGameData:match.matchData forPlayerWithId:[GKLocalPlayer localPlayer].playerID allPlayers:[GCTurnBasedMatchHelper sharedInstance].currentPlayerIds onlyActions:NO onlyEnemyUnits:NO];
    
    if ([GameManager sharedManager].currentGame.state == kGameStateInitialState ||
        [GameManager sharedManager].currentGame.state == kGameStateFinishedPlacingCards) {
        [self.view presentScene:[HKConstructDeckScene sceneWithSize:self.size] transition:[SKTransition crossFadeWithDuration:0.5]];
    }
    else if ([GameManager sharedManager].currentGame.state == kGameStateGameStarted) {
        [self.view presentScene:[HKGameScene sceneWithSize:self.size] transition:[SKTransition crossFadeWithDuration:0.5]];
    }
}

- (void)layoutMatch:(GKTurnBasedMatch *)match {
    
    NSLog(@"Other players turn");
    
    [[GameManager sharedManager] continueExistingGame];
    [[GameManager sharedManager].currentGame deserializeGameData:match.matchData forPlayerWithId:[GKLocalPlayer localPlayer].playerID allPlayers:[GCTurnBasedMatchHelper sharedInstance].currentPlayerIds onlyActions:NO onlyEnemyUnits:NO];
    [self.view presentScene:[HKGameScene sceneWithSize:self.size] transition:[SKTransition crossFadeWithDuration:0.5]];
}

@end
