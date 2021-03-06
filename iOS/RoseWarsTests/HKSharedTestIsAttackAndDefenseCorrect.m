//
//  HKSharedTestIsAttackAndDefenseCorrect.m
//  RoseWars
//
//  Created by Heine Kristensen on 08/02/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <XCTest/XCTest.h>
#import "HKSharedTestIsAttackAndDefenseCorrect.h"
#import "HKSharedTestBaseExecuter.h"
#import "PathFinder.h"
#import "GameBoardMockup.h"
#import "MeleeAttackAction.h"
#import "BaseRangedAttribute.h"
#import "HKAttribute.h"

@implementation HKSharedTestIsAttackAndDefenseCorrect

- (BOOL)executeSharedTestWithData:(NSDictionary *)data {
    [super executeSharedTestWithData:data];
    
    NSDictionary *actiondata = data[@"action"];
    
    NSInteger minimumAttackRequired = [data[@"attack"] integerValue];
    NSInteger minimumDefenceRequired = [data[@"defence"] integerValue];
    
    GridLocation *startLocation = [self convertLocation:actiondata[@"start_at"]];
    GridLocation *targetLocation = [self convertLocation:actiondata[@"target_at"]];
    
    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    Card *attacker = [self.gamemanager cardLocatedAtGridLocation:startLocation];
    Card *defender = [self.gamemanager cardLocatedAtGridLocation:targetLocation];
    
    Action *action;
    
    if (attacker.isMelee) {
        action = [pathfinder getMeleeAttackActionForCard:attacker
                                       againstEnemyUnit:defender];
    }
    else if(attacker.isRanged) {
        action = (Action*)[pathfinder getRangedAttackActionForCard:attacker
                                         againstEnemyUnit:defender];
    }

    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    action.delegate = mock;
    
    __block BOOL testSucceeded = NO;
    dispatch_semaphore_t semaphore = dispatch_semaphore_create(0);
    [action performActionWithCompletion:^{
        NSInteger attackValue = [attacker.attack calculateValue];
        NSInteger defendValue = [defender.defence calculateValue];

        BOOL attackSuccess = attackValue <= minimumAttackRequired;
        BOOL defenceSuccess = defendValue <= minimumDefenceRequired;
        testSucceeded = attackSuccess && defenceSuccess;
        dispatch_semaphore_signal(semaphore);
    }];
    
    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
    
    return testSucceeded;
}

@end
