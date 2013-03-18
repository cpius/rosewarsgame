//
//  RangedAttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/17/13.
//
//

#import "RangedAttackAction.h"
#import "GameManager.h"
#import "StandardBattleStrategy.h"

@implementation RangedAttackAction
@synthesize actionType = _actionType;
@synthesize startLocation = _startLocation;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _actionType = kActionTypeRanged;
        _startLocation = card.cardLocation;
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

    CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard battleStrategy:self.cardInAction.battleStrategy];
    
    self.combatOutcome = combatOutcome;
    [self.delegate action:self hasResolvedCombatWithOutcome:combatOutcome];
        
    [[GameManager sharedManager] actionUsed:self];
    [self.cardInAction didPerformedAction:self];
    
    [self.delegate afterPerformAction:self];

    if (completion != nil) {
        completion();
    }
}

@end
