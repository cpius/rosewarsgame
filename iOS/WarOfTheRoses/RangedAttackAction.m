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
@synthesize battleReport = _battleReport;

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
    
    _battleReport = [BattleReport battleReportWithAction:self];

    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];

    BattleResult *result = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard battleStrategy:self.cardInAction.battleStrategy];
    
    _battleReport.primaryBattleResult = result;
    
    self.battleResult = result;
    [self.delegate action:self hasResolvedCombatWithOutcome:result.combatOutcome];
        
    [[GameManager sharedManager] actionUsed:self];
    [self.cardInAction didPerformedAction:self];
    
    [[GameManager sharedManager].currentGame setLatestBattleReport:_battleReport];

    [self.delegate afterPerformAction:self];

    if (completion != nil) {
        completion();
    }
}

@end
