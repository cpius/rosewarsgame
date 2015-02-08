//
//  AttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "MeleeAttackAction.h"
#import "GridLocation.h"
#import "PathFinderStep.h"
#import "GameManager.h"
#import "StandardBattleStrategy.h"
#import "PushAction.h"

@implementation MeleeAttackAction

@synthesize meleeAttackType = _meleeAttackType;
@synthesize actionType = _actionType;
@synthesize startLocation = _startLocation;
@synthesize battleReport = _battleReport;
@synthesize enemyInitialLocation = _enemyInitialLocation;
@synthesize gamemanager = _gamemanager;

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    return [self initWithGameManager:gamemanager path:path andCardInAction:card enemyCard:enemyCard meleeAttackType:kMeleeAttackTypeConquer];
}

- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard meleeAttackType:(MeleeAttackTypes)meleeAttackType {
    
    self = [super initWithGameManager:gamemanager path:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _gamemanager = gamemanager;
        _actionType = kActionTypeMelee;
        _meleeAttackType = meleeAttackType;
        
        _startLocation = card.cardLocation;
        _enemyInitialLocation = enemyCard.cardLocation;
        _gridLocationForConquer = enemyCard.cardLocation;
        
        _secondaryActionsForPlayback = [NSMutableDictionary dictionary];
    }
    
    return self;
}

- (BOOL)isAttack {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return kActionTypeMelee;
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
    
    GridLocation *retreatLocation = [self getEntryLocationInPath];
    
    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        [self.cardInAction consumeMoves:self.path.count];
        
        BattleResult *result = [self.gamemanager resolveCombatBetween:self.cardInAction defender:self.enemyCard battleStrategy:self.cardInAction.battleStrategy];
        
        [self.cardInAction didResolveCombatDuringAction:self];
        
        // Default to normal attack type
        result.meleeAttackType = kMeleeAttackTypeNormal;
        
        self.battleResult = result;
        [self.delegate action:self hasResolvedCombatWithResult:result];
        
        _battleReport.primaryBattleResult = result;

        [self.gamemanager.currentGame addBattleReport:_battleReport forAction:self];

        if (IsDefenseSuccessful(result.combatOutcome)) {
            
            PathFinderStep *retreatToLocation = [[PathFinderStep alloc] initWithLocation:retreatLocation];
            
            [self.delegate action:self wantsToMoveFollowingPath:@[retreatToLocation] withCompletion:^(GridLocation *endLocation) {
                
                if (![self.cardInAction.cardLocation isSameLocationAs:retreatLocation]) {
                    [self.gamemanager card:self.cardInAction movedToGridLocation:retreatLocation];
                    [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:_startLocation toLocation:retreatLocation];
                }
                
                [self afterPerformAction];
                if (completion != nil) {
                    completion();
                    return;
                }
            }];
        }
        else {
        /*    if (_meleeAttackType == kMeleeAttackTypeConquer && self.enemyCard.dead) {
                [self afterPerformAction];
                if (self.autoConquer) {
                    [self conquerEnemyLocation:self.enemyCard.cardLocation withCompletion:^{
                        completion();
                        return;
                    }];
                }
                else {
                    completion();
                    return;
                }
            }*/
            if (IsPushSuccessful(result.combatOutcome) && !self.enemyCard.dead) {
                
                [PushAction performPushFromAction:self gameManager:self.gamemanager withCompletion:^{
                    if (self.meleeAttackStrategy == kMeleeAttackStrategyAutoConquer && ![self.gamemanager isCardLocatedAtGridLocation:_enemyInitialLocation]) {
                        [self conquerEnemyLocationWithCompletion:^{
                            if (completion != nil) {
                                completion();
                                return;
                            }
                        }];
                    }
                    else {
                        [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:retreatLocation]] withCompletion:^(GridLocation *endLocation) {
                            
                            [self.gamemanager card:self.cardInAction movedToGridLocation:retreatLocation];
                            
                            if (![_startLocation isEqual:retreatLocation]) {
                                [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:_startLocation toLocation:retreatLocation];
                            }
                            
                            [self afterPerformAction];
                            if (completion != nil) {
                                completion();
                                return;
                            }
                        }];
                    }
                }];
            }
            else {
                [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:retreatLocation]] withCompletion:^(GridLocation *endLocation) {
                    
                    [self.gamemanager card:self.cardInAction movedToGridLocation:retreatLocation];
                    
                    if (![_startLocation isEqual:retreatLocation]) {
                        [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:_startLocation toLocation:retreatLocation];
                    }
                    
                    if (self.meleeAttackStrategy == kMeleeAttackStrategyAutoConquer) {
                        [self conquerEnemyLocationWithCompletion:^{
                            [self afterPerformAction];
                            if (completion != nil) {
                                completion();
                                return;
                            }
                        }];
                        
                        return;
                    }
                    
                    [self afterPerformAction];
                    if (completion != nil) {
                        completion();
                        return;
                    }
                }];
            }
        }
    }];
}

- (BOOL)unitCanConquerEnemyLocation {
    
    // If attack or push is successful
    return (IsAttackSuccessful(self.battleReport.primaryBattleResult.combatOutcome) && self.meleeAttackType == kMeleeAttackTypeConquer && self.enemyCard.dead) ||
            (IsPushSuccessful(self.battleReport.primaryBattleResult.combatOutcome));
}

- (void)conquerEnemyLocationWithCompletion:(void (^)())completion {

    if (_meleeAttackType == kMeleeAttackTypeNormal) {
        // Conquer not possible in this attack, just call completion at once
        if (completion != nil) {
            completion();
        }
    }
    else {
        self.battleResult.meleeAttackType = kMeleeAttackTypeConquer;
        
        GridLocation *cardInActionStartLocation = self.cardInAction.cardLocation;

        [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:self.gridLocationForConquer]] withCompletion:^(GridLocation *endLocation) {
            [self.gamemanager card:self.cardInAction movedToGridLocation:endLocation];
            [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:cardInActionStartLocation toLocation:endLocation];
            if (completion != nil) {
                completion();
            }
        }];
    }
}

- (void)cardIncreasedInLevel:(Card *)card withAbilityIncreased:(LevelIncreaseAbilities)ability {
    
    if (!self.playback) {
        _battleReport.levelIncreased = YES;
        _battleReport.abilityIncreased = ability;
    }
}

- (void)afterPerformAction {
    
    self.cardInAction.delegate = nil;
    
    [self.gamemanager actionUsed:self];
    [self.cardInAction didPerformedAction:self];
}

@end
