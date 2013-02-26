//
//  RangedAttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/17/13.
//
//

#import "RangedAttackAction.h"

@implementation RangedAttackAction

- (BOOL)isWithinRange {
    
    return self.path.count <= self.cardInAction.range;
}

- (BOOL)isAttack {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return kActionTypeRanged;
}

- (void)performAction {
    
/*    [self.delegate beforePerformAction:self];
    
    CombatOutcome outcome = [self engageCombatBetweenMyCard:action.cardInAction andEnemyCard:action.enemyCard];
    
    if (outcome == kCombatOutcomeDefendSuccessful) {
        [self resetUserInterface];
    }
    else {
        [ParticleHelper applyBurstToNode:targetNode];
        
        [_gameManager cardHasBeenDefeated:action.enemyCard];
        [_gameboard removeCardAtGameBoardNode:targetNode];
        [self resetUserInterface];
    }
        
    [self.delegate afterPerformAction:self];*/
}

@end
