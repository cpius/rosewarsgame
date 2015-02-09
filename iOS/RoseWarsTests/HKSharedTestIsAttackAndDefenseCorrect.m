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

@implementation HKSharedTestIsAttackAndDefenseCorrect

- (BOOL)executeSharedTestWithData:(NSDictionary *)data {
    [super executeSharedTestWithData:data];
    
    NSDictionary *actiondata = data[@"action"];
    
    NSInteger minimumAttackRequired = [data[@"attack"] integerValue];
    NSInteger maximumDefenceRequired = [data[@"defence"] integerValue];
    
    GridLocation *startLocation = [self convertLocation:actiondata[@"start_at"]];
    GridLocation *endLocation = [self convertLocation:actiondata[@"end_at"]];
    GridLocation *targetLocation = [self convertLocation:actiondata[@"target_at"]];
    
    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    Card *attacker = [self.gamemanager cardLocatedAtGridLocation:startLocation];
    Card *defender = [self.gamemanager cardLocatedAtGridLocation:targetLocation];
    
    Action *action;
    
    if (attacker.isMelee) {
        action = [pathfinder getMeleeAttackActionForCard:attacker
                                       againstEnemyUnit:defender
                                           allLocations:self.gamemanager.currentGame.unitLayout];
    }
    else if(attacker.isRanged) {
        action = (Action*)[pathfinder getRangedAttackActionForCard:attacker
                                         againstEnemyUnit:defender
                                             allLocations:self.gamemanager.currentGame.unitLayout];
    }

    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    action.delegate = mock;
    
    __block BOOL testSucceeded = NO;
    dispatch_semaphore_t semaphore = dispatch_semaphore_create(0);
    [action performActionWithCompletion:^{
        AttributeRange attackValue = [attacker.attack calculateValue];
        AttributeRange defendValue = [defender.defence calculateValue];

        BOOL attackSuccess = minimumAttackRequired >= attackValue.lowerValue && minimumAttackRequired <= attackValue.upperValue;
        BOOL defenceSuccess = maximumDefenceRequired >= defendValue.lowerValue && maximumDefenceRequired <= defendValue.upperValue;
        testSucceeded = attackSuccess && defenceSuccess;
        dispatch_semaphore_signal(semaphore);
    }];
    
    dispatch_semaphore_wait(semaphore, DISPATCH_TIME_FOREVER);
    
    return testSucceeded;
}

@end
