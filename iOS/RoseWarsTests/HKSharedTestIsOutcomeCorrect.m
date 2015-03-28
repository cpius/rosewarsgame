//
//  HKSharedTestIsOutcomeCorrect.m
//  RoseWars
//
//  Created by Heine Kristensen on 10/02/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <XCTest/XCTest.h>
#import "HKSharedTestIsOutcomeCorrect.h"
#import "PathFinder.h"
#import "Action.h"
#import "GameBoardMockup.h"
#import "MeleeAttackAction.h"
#import "BaseRangedAttribute.h"
#import "HKAttribute.h"
#import "FixedDiceStrategy.h"
#import "BaseBattleStrategy.h"
#import "BattlePlan.h"
#import "MoveAction.h"
#import "Game.h"

@implementation HKSharedTestIsOutcomeCorrect

- (BOOL)executeSharedTestWithData:(NSDictionary *)data {
    [super executeSharedTestWithData:data];
    
    NSDictionary *outcome = data[@"outcome"];
    NSDictionary *actiondata = data[@"action"];
    NSDictionary *preGameState = data[@"pre_gamestate"];
    NSDictionary *postGameState = data[@"post_gamestate"];
    
    NSDictionary *player1Units = preGameState[@"player1_units"];
    NSDictionary *player2Units = preGameState[@"player2_units"];
    
    [self setupBoardWithPlayer1Units:player1Units player2Units:player2Units];
    
    GridLocation *startLocation = [self convertLocation:actiondata[@"start_at"]];
    GridLocation *targetLocation = [self convertLocation:actiondata[@"target_at"]];
    GridLocation *endLocation = [self convertLocation:actiondata[@"end_at"]];

    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *rolls = outcome[actiondata[@"target_at"]];

    Card *attacker = [self.gamemanager cardLocatedAtGridLocation:startLocation];
    Card *defender = [self.gamemanager cardLocatedAtGridLocation:targetLocation];
    
    Action *action;
    if (defender) {
        attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:[rolls[0] integerValue]];
        defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:[rolls[1] integerValue]];

        if (attacker.isMelee) {
            MeleeAttackAction *melee = [pathfinder getMeleeAttackActionForCard:attacker
                                                              againstEnemyUnit:defender];
            melee.meleeAttackStrategy = kMeleeAttackStrategyAutoConquer;
            action = melee;
            
        }
        else if(attacker.isRanged) {
            action = (Action*)[pathfinder getRangedAttackActionForCard:attacker
                                                      againstEnemyUnit:defender];
        }
    }
    else {
        action = [pathfinder getMoveActionFromLocation:startLocation forCard:attacker toLocation:endLocation enemyUnits:self.gamemanager.currentGame.enemyDeck.cards];
    }
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    action.delegate = mock;
    
    [self checkPreGameState:preGameState];
    
    __block BOOL testSucceeded = NO;
    dispatch_semaphore_t semaphore = dispatch_semaphore_create(0);
    [action performActionWithCompletion:^{
        testSucceeded = [self checkPostGameState:postGameState];
        dispatch_semaphore_signal(semaphore);
    }];
    
    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
    
    return testSucceeded;
}

- (void)checkPreGameState:(NSDictionary*)preGameState {
    if (preGameState[@"actions_remaining"]) {
        NSInteger actionsRemaining = [preGameState[@"actions_remaining"] integerValue];
        XCTAssert(actionsRemaining == self.gamemanager.currentGame.numberOfAvailableActions, @"Wrong number of available actions");
    }
}

- (BOOL)checkPostGameState:(NSDictionary*)postGameState {
    BOOL success = YES;
    if (postGameState[@"actions_remaining"]) {
        NSInteger actionsRemaining = [postGameState[@"actions_remaining"] integerValue];
        success = actionsRemaining == [self numberOfActionsAvailable];
        XCTAssert(success, @"Wrong number of available actions");
    }
    
    NSDictionary *player1Units = postGameState[@"player1_units"];
//    NSDictionary *player2Units = postGameState[@"player2_units"];
    
    for (NSString *key in player1Units.allKeys) {
        NSDictionary *dictionary = player1Units[key];
        
        Card *card = [self.gamemanager cardLocatedAtGridLocation:[self convertLocation:key]];
        if (dictionary[@"experience"]) {
            NSUInteger experience = [dictionary[@"experience"] integerValue];
            success = experience == card.experience;
            XCTAssert(success, @"Wrong number of experience points");
        }
        
        if (dictionary[@"used"]) {
            BOOL used = dictionary[@"used"];
            success = used == card.hasPerformedActionThisRound;
            XCTAssert(success);
        }
    }

    return success;
}

- (NSUInteger)numberOfActionsAvailable {
    NSUInteger totalNumberOfActions = 0;
    for (Card *unit in self.gamemanager.currentGame.myDeck.cards) {
        BattlePlan *battleplan = [[BattlePlan alloc] initWithGame:self.gamemanager];
        [battleplan createBattlePlanForCard:unit friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards];
        totalNumberOfActions += [battleplan totalNumberOfActions];
    }
    
    return totalNumberOfActions;
}

@end
