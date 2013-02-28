//
//  RangedAttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/17/13.
//
//

#import "RangedAttackAction.h"
#import "GameManager.h"

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

- (void)performActionWithCompletion:(void (^)())completion {
    
    [self.delegate beforePerformAction:self];

    CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard];
    
    [self.delegate action:self hasResolvedRangedCombatWithOutcome:combatOutcome];
        
    [self.cardInAction performedAction:self];
    [[GameManager sharedManager] actionUsed:self];
    
    [self.delegate afterPerformAction:self];

    if (completion != nil) {
        completion();
    }
}

@end
