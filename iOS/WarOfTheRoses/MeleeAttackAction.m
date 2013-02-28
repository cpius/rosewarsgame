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

@implementation MeleeAttackAction

@synthesize meleeAttackType;

- (BOOL)isWithinRange {
    
    return self.path.count <= self.cardInAction.movesRemaining;
}

- (BOOL)isAttack {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return kActionTypeMelee;
}


- (void)performActionWithCompletion:(void (^)())completion {
    
    [self.delegate beforePerformAction:self];
    
    GridLocation *retreatLocation = self.cardInAction.cardLocation;
    GridLocation *startLocation = self.cardInAction.cardLocation;
    
    if (self.path.count > 1) {
        retreatLocation = [[self.path objectAtIndex:self.path.count - 2] location];
    }

    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard];
        
        [self.delegate action:self hasResolvedRangedCombatWithOutcome:combatOutcome];
        
        if (IsDefenseSuccessful(combatOutcome)) {
            
            PathFinderStep *retreatToLocation = [[PathFinderStep alloc] initWithLocation:retreatLocation];
            
            [self.delegate action:self wantsToMoveFollowingPath:@[retreatToLocation] withCompletion:^(GridLocation *endLocation) {
                
                if (![self.cardInAction.cardLocation isEqual:retreatLocation]) {
                    [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
                    [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:startLocation toLocation:retreatLocation];
                }
                
                [self.cardInAction performedAction:self];
                [[GameManager sharedManager] actionUsed:self];
                
                [self.delegate afterPerformAction:self];

                if (completion != nil) {
                    completion();
                }
            }];
        }
        else {
            
            if (meleeAttackType == kMeleeAttackTypeNormal) {
                
                [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:retreatLocation]] withCompletion:^(GridLocation *endLocation) {
                    
                    [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
                    
                    if (![startLocation isEqual:retreatLocation]) {
                        [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:startLocation toLocation:retreatLocation];
                    }
                    
                    [self.cardInAction performedAction:self];
                    [[GameManager sharedManager] actionUsed:self];
                    
                    [self.delegate afterPerformAction:self];

                    if (completion != nil) {
                        completion();
                    }
                }];
            }
            else {
                
                [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:self.enemyCard.cardLocation];
                [self.delegate action:self wantsToReplaceCardAtLocation:self.enemyCard.cardLocation withCardAtLocation:startLocation];
                
                [self.cardInAction performedAction:self];
                [[GameManager sharedManager] actionUsed:self];
                
                [self.delegate afterPerformAction:self];

                if (completion != nil) {
                    completion();
                }
            }
        }
    }];
}

@end
