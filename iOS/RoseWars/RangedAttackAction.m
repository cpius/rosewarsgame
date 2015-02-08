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

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithGameManager:gamemanager path:path andCardInAction:card enemyCard:enemyCard];
    
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

- (NSUInteger)cost {
    
    return self.cardInAction.attackActionCost;
}

- (void)performActionWithCompletion:(void (^)())completion {
    
    _battleReport = [BattleReport battleReportWithAction:self];
    
    self.cardInAction.delegate = self;

    [self.gamemanager willUseAction:self];
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];

    BattleResult *result = [self.gamemanager resolveCombatBetween:self.cardInAction defender:self.enemyCard battleStrategy:self.cardInAction.battleStrategy];
    
    [self.cardInAction didResolveCombatDuringAction:self];
    
    _battleReport.primaryBattleResult = result;
    
    self.battleResult = result;
    [self.delegate action:self hasResolvedCombatWithResult:result];
        
    [self.gamemanager actionUsed:self];
    [self.cardInAction didPerformedAction:self];
    
    [self.gamemanager.currentGame addBattleReport:_battleReport forAction:self];

    [self.delegate afterPerformAction:self];
    self.cardInAction.delegate = nil;
    
    if (completion != nil) {
        completion();
    }
}

- (void)cardIncreasedInLevel:(Card *)card withAbilityIncreased:(LevelIncreaseAbilities)ability {
    
    if (!self.playback) {
        _battleReport.levelIncreased = YES;
        _battleReport.abilityIncreased = ability;
    }
}

@end
