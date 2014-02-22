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

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    return [self initWithPath:path andCardInAction:card enemyCard:enemyCard meleeAttackType:kMeleeAttackTypeConquer];
}

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard meleeAttackType:(MeleeAttackTypes)meleeAttackType {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _actionType = kActionTypeMelee;
        _meleeAttackType = meleeAttackType;
        
        _startLocation = card.cardLocation;
        _enemyInitialLocation = enemyCard.cardLocation;
        
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

    [[GameManager sharedManager] willUseAction:self];
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    GridLocation *retreatLocation = [self getEntryLocationInPath];
    
    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        [self.cardInAction consumeMoves:self.path.count];
        
        BattleResult *result = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard battleStrategy:self.cardInAction.battleStrategy];
        
        result.meleeAttackType = self.meleeAttackType;
        
        self.battleResult = result;
        [self.delegate action:self hasResolvedCombatWithResult:result];
        
        _battleReport.primaryBattleResult = result;

        [[GameManager sharedManager].currentGame addBattleReport:_battleReport forAction:self];

        if (IsDefenseSuccessful(result.combatOutcome)) {
            
            PathFinderStep *retreatToLocation = [[PathFinderStep alloc] initWithLocation:retreatLocation];
            
            [self.delegate action:self wantsToMoveFollowingPath:@[retreatToLocation] withCompletion:^(GridLocation *endLocation) {
                
                if (![self.cardInAction.cardLocation isSameLocationAs:retreatLocation]) {
                    [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
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
            if (_meleeAttackType == kMeleeAttackTypeConquer && self.enemyCard.dead) {
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
            }
            else if (IsPushSuccessful(result.combatOutcome) && !self.enemyCard.dead) {
                
                [PushAction performPushFromAction:self withCompletion:^{
                    if (self.autoConquer && [[GameManager sharedManager] cardLocatedAtGridLocation:_enemyInitialLocation] == nil) {
                        [self conquerEnemyLocation:_enemyInitialLocation withCompletion:^{
                            if (completion != nil) {
                                completion();
                                return;
                            }
                        }];
                    }
                    else {
                        [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:retreatLocation]] withCompletion:^(GridLocation *endLocation) {
                            
                            [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
                            
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
                    
                    [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
                    
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
        }
    }];
}

- (BOOL)unitCanConquerEnemyLocation {
    
    return IsAttackSuccessful(self.battleReport.primaryBattleResult.combatOutcome) && self.meleeAttackType == kMeleeAttackTypeConquer;
}

- (void)conquerEnemyLocation:(GridLocation*)enemyLocation withCompletion:(void (^)())completion {

    if (_meleeAttackType == kMeleeAttackTypeNormal) {
        // Conquer not possible in this attack, just call completion at once
        completion();
    }
    else {
        [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:enemyLocation]] withCompletion:^(GridLocation *endLocation) {
            [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:enemyLocation];
            [self.delegate action:self wantsToReplaceCardAtLocation:enemyLocation withCardAtLocation:_startLocation];
            
            completion();
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
    
    [[GameManager sharedManager] actionUsed:self];
    [self.cardInAction didPerformedAction:self];
}

@end
