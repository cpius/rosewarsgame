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
@synthesize actionType = _actionType;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard {
    
    self = [super initWithPath:path andCardInAction:card enemyCard:enemyCard];
    
    if (self) {
        _actionType = kActionTypeMelee;
    }
    
    return self;
}

- (BOOL)isAttack {
    
    return YES;
}

- (ActionTypes)actionType {
    
    return kActionTypeMelee;
}


- (void)performActionWithCompletion:(void (^)())completion {
    
    [self.cardInAction willPerformAction:self];
    [self.delegate beforePerformAction:self];
    
    GridLocation *retreatLocation = self.cardInAction.cardLocation;
    GridLocation *startLocation = self.cardInAction.cardLocation;
    
    if (self.path.count > 1) {
        retreatLocation = [[self.path objectAtIndex:self.path.count - 2] location];
    }

    [self.delegate action:self wantsToMoveFollowingPath:self.path withCompletion:^(GridLocation *endLocation) {
        
        [self.cardInAction consumeMoves:self.path.count];
        
        CombatOutcome combatOutcome = [[GameManager sharedManager] resolveCombatBetween:self.cardInAction defender:self.enemyCard];
        
        self.combatOutcome = combatOutcome;
        [self.delegate action:self hasResolvedRangedCombatWithOutcome:combatOutcome];
        
        if (IsDefenseSuccessful(combatOutcome)) {
            
            PathFinderStep *retreatToLocation = [[PathFinderStep alloc] initWithLocation:retreatLocation];
            
            [self.delegate action:self wantsToMoveFollowingPath:@[retreatToLocation] withCompletion:^(GridLocation *endLocation) {
                
                if (![self.cardInAction.cardLocation isEqual:retreatLocation]) {
                    [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
                    [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:startLocation toLocation:retreatLocation];
                }
                
                [[GameManager sharedManager] actionUsed:self];
               [self.cardInAction didPerformedAction:self];
                
                [self.delegate afterPerformAction:self];

                if (completion != nil) {
                    completion();
                }
            }];
        }
        else {
            
            if (meleeAttackType == kMeleeAttackTypeConquer && self.enemyCard.dead) {
                
                [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:self.enemyCard.cardLocation];
                [self.delegate action:self wantsToReplaceCardAtLocation:self.enemyCard.cardLocation withCardAtLocation:startLocation];
                
                [[GameManager sharedManager] actionUsed:self];
                [self.cardInAction didPerformedAction:self];
                
                [self.delegate afterPerformAction:self];
                
                if (completion != nil) {
                    completion();
                }
            }
            else {
                [self.delegate action:self wantsToMoveFollowingPath:@[[[PathFinderStep alloc] initWithLocation:retreatLocation]] withCompletion:^(GridLocation *endLocation) {
                    
                    [[GameManager sharedManager] card:self.cardInAction movedToGridLocation:retreatLocation];
                    
                    if (![startLocation isEqual:retreatLocation]) {
                        [self.delegate action:self wantsToMoveCard:self.cardInAction fromLocation:startLocation toLocation:retreatLocation];
                    }
                    
                    [[GameManager sharedManager] actionUsed:self];
                    [self.cardInAction didPerformedAction:self];
                    
                    [self.delegate afterPerformAction:self];
                    
                    if (completion != nil) {
                        completion();
                    }
                }];
            }
        }
    }];
}

@end
