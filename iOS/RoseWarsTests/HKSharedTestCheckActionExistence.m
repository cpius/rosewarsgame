//
//  HKSharedTestCheckActionExistence.m
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKSharedTestCheckActionExistence.h"
#import "PathFinder.h"
#import "BattlePlan.h"
#import "PathFinderStrategyFactory.h"
#import "Action.h"
#import "MeleeAttackAction.h"

@implementation HKSharedTestCheckActionExistence

- (BOOL)executeSharedTestWithData:(NSDictionary *)data {
    
    NSLog(@"Executing shared test: '%@'", data[@"description"]);
    
    if ([data[@"description"] isEqualToString:@"test if Scout can move past Pikemen"]) {
        NSLog(@"dfdf");
    }

    BOOL executeSuccess = [super executeSharedTestWithData:data];
    
    NSDictionary *actiondata = data[@"action"];
    
    NSInteger expectedOutcome = [data[@"result"] integerValue];

    GridLocation *startLocation = [self convertLocation:actiondata[@"start_at"]];
    GridLocation *endLocation = [self convertLocation:actiondata[@"end_at"]];
    GridLocation *targetLocation = [self convertLocation:actiondata[@"target_at"]];
    
    BattlePlan *battleplan = [[BattlePlan alloc] init];
    
    Card *cardLocatedAtStartLocation = [self.gamemanager cardLocatedAtGridLocation:startLocation];
    
    [battleplan createBattlePlanForCard:cardLocatedAtStartLocation friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards unitLayout:self.gamemanager.currentGame.unitLayout];

    Action *action;
    
    if (targetLocation != nil) {
        action = [battleplan getActionToGridLocation:targetLocation];
    }
    else {
        action = [battleplan getActionToGridLocation:endLocation];
    }

    BOOL moveWithAttack = [actiondata[@"move_with_attack"] integerValue] == 1 ? YES : NO;
    if (cardLocatedAtStartLocation.isMelee) {
    
        MeleeAttackAction *meleeAction = (MeleeAttackAction*)action;
        
        if (meleeAction && moveWithAttack) {
            return [self evaluateOutcomeFromExpectedOutcome:expectedOutcome actualOutcome:meleeAction.meleeAttackType == kMeleeAttackTypeConquer];
       }
        
        action = meleeAction;
    }
    
    if (cardLocatedAtStartLocation.isRanged) {
        if (moveWithAttack) {
            return [self evaluateOutcomeFromExpectedOutcome:expectedOutcome actualOutcome:NO];
        }
    }
    
    return [self evaluateOutcomeFromExpectedOutcome:expectedOutcome actualOutcome:action != nil];
}

@end
