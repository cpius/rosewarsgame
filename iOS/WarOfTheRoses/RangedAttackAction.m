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
@synthesize actionType = _actionType;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _actionType = kActionTypeRanged;
    }
    
    return self;
}

- (BOOL)isAttack {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return kActionTypeRanged;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];

    CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard];
    
    self.combatOutcome = combatOutcome;
    [self.delegate action:self hasResolvedRangedCombatWithOutcome:combatOutcome];
        
    [[GameManager sharedManager] actionUsed:self];
    [self.cardInAction didPerformedAction:self];
    
    [self.delegate afterPerformAction:self];

    if (completion != nil) {
        completion();
    }
}

@end
