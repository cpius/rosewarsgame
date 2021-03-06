//
//  BattlePlan.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import "BattlePlan.h"
#import "PathFinder.h"
#import "GameManager.h"
#import "PathFinderStrategyFactory.h"
#import "MeleeAttackAction.h"
#import "GameManager.h"

@implementation BattlePlan

- (instancetype)init {
    NSAssert(YES, @"use initWithGame");
    return nil;
}

- initWithGame:(GameManager*)gamemanager {
    
    self = [super init];
    
    if (self) {
        NSAssert(gamemanager, @"Game must be non-nil");
        _gamemanager = gamemanager;
    }
    
    return self;
}

- (BOOL)isGrindLocationInsideGameBoard:(GridLocation *)location {
    
    if (location.column >= 1 &&
        location.column <= BOARDSIZE_COLUMNS &&
        location.row >= 1 &&
        location.row <= BOARDSIZE_ROWS) {
        return YES;
    }
    
    return NO;
}

- (NSDictionary *)getAttackDirectionsAction:(MeleeAttackAction*)action {
    
    NSMutableDictionary *attackDirections = [NSMutableDictionary dictionary];
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    // Add location of target
    [attackDirections setObject:action.path forKey:action.enemyCard.cardLocation];
    
    NSArray *surroundingLocations = [action.enemyCard.cardLocation surroundingGridLocations];
    
    for (GridLocation *location in surroundingLocations) {
        
        Card *cardInLocation = [self.gamemanager.currentGame.unitLayout objectForKey:location];
        
        if (cardInLocation == nil && [location isInsideGameBoard]) {

            NSArray *path = [pathFinder getPathForCard:action.cardInAction fromGridLocation:action.cardInAction.cardLocation toGridLocation:location usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategyWithMeleeAttackType:action.meleeAttackType]];
            
            if (path != nil) {
                NSMutableArray *newPath = [NSMutableArray arrayWithArray:path];
                // And add last step from enemy unit
                [newPath addObject:[[PathFinderStep alloc] initWithLocation:action.enemyCard.cardLocation]];
                
                MeleeAttackAction *tempAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:newPath andCardInAction:action.cardInAction enemyCard:action.enemyCard meleeAttackType:action.meleeAttackType];
                
                if ([action.cardInAction allowAction:tempAction allLocations:self.gamemanager.currentGame.unitLayout]) {
                    [attackDirections setObject:newPath forKey:location];
                }
            }
        }
    }
    
    return attackDirections;
}

- (Action*)getActionToGridLocation:(GridLocation*)gridLocation {
    
    Action *foundAction = nil;
    
    for (Action *moveAction in _moveActions) {
        if ([[moveAction getLastLocationInPath] isSameLocationAs:gridLocation]) {
            foundAction = moveAction;
            break;
        }
    }
    
    for (Action *meleeAction in _meleeActions) {
        if ([[meleeAction getLastLocationInPath] isSameLocationAs:gridLocation]) {
            foundAction = meleeAction;
            break;
        }
    }
    
    for (Action *rangeAction in _rangeActions) {
        if ([[rangeAction getLastLocationInPath] isSameLocationAs:gridLocation]) {
            foundAction = rangeAction;
            break;
        }
    }
    
    for (Action *abilityAction in _abilityActions) {
        if ([[abilityAction getLastLocationInPath] isSameLocationAs:gridLocation]) {
            foundAction = abilityAction;
            break;
        }
    }
    
    return foundAction;
}

- (NSArray *)createBattlePlanForCard:(Card *)card friendlyUnits:(NSArray*)friendlyUnits enemyUnits:(NSArray *)enemyUnits {
    
    if (![card isOwnedByCurrentPlayer]) return [NSArray array];
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:_gamemanager];
    
    NSUInteger remainingActionCount = self.gamemanager.currentGame.numberOfAvailableActions;
    
    if ([card canPerformActionOfType:kActionTypeMove withRemainingActionCount:remainingActionCount]) {
        _moveActions = [pathFinder getMoveActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits];
    }
    
    if ([card canPerformActionOfType:kActionTypeMelee withRemainingActionCount:remainingActionCount]) {
        _meleeActions = [pathFinder getMeleeAttackActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits];
    }

    if ([card canPerformActionOfType:kActionTypeRanged withRemainingActionCount:remainingActionCount]) {
        _rangeActions = [pathFinder getRangedAttackActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits];
    }
    
    if ([card canPerformActionOfType:kActionTypeAbility withRemainingActionCount:remainingActionCount]) {
        _abilityActions = [pathFinder getAbilityActionsFromLocation:card.cardLocation forCard:card friendlyUnits:friendlyUnits enemyUnits:enemyUnits];
    }
    
    return [[[_moveActions arrayByAddingObjectsFromArray:_meleeActions] arrayByAddingObjectsFromArray:_rangeActions] arrayByAddingObjectsFromArray:_abilityActions];
}

- (BOOL)hasActions {
    
    return _moveActions.count > 0 ||
    _meleeActions.count > 0 ||
    _rangeActions.count > 0 ||
    _abilityActions.count > 0;
}

- (NSInteger)totalNumberOfActions {
    return _moveActions.count +
    _meleeActions.count +
    _rangeActions.count +
    _abilityActions.count;
}

@end
