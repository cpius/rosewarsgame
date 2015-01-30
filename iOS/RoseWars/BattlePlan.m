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
#import "Game.h"

@implementation BattlePlan

- initWithGame:(Game*)game {
    
    self = [super init];
    
    if (self) {
        NSAssert(game, @"Game must be non-nil");
        _game = game;
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

- (NSDictionary *)getAttackDirectionsAction:(MeleeAttackAction*)action withUnitLayout:(NSDictionary*)unitLayout {
    
    NSMutableDictionary *attackDirections = [NSMutableDictionary dictionary];
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    // Add location of target
    [attackDirections setObject:action.path forKey:action.enemyCard.cardLocation];
    
    NSArray *surroundingLocations = [action.enemyCard.cardLocation surroundingGridLocations];
    
    for (GridLocation *location in surroundingLocations) {
        
        Card *cardInLocation = [unitLayout objectForKey:location];
        
        if (cardInLocation == nil && [location isInsideGameBoard]) {

            NSArray *path = [pathFinder getPathForCard:action.cardInAction fromGridLocation:action.cardInAction.cardLocation toGridLocation:location usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategyWithMeleeAttackType:action.meleeAttackType] allLocations:[GameManager sharedManager].currentGame.unitLayout];
            
            if (path != nil) {
                NSMutableArray *newPath = [NSMutableArray arrayWithArray:path];
                // And add last step from enemy unit
                [newPath addObject:[[PathFinderStep alloc] initWithLocation:action.enemyCard.cardLocation]];
                
                MeleeAttackAction *tempAction = [[MeleeAttackAction alloc] initWithPath:newPath andCardInAction:action.cardInAction enemyCard:action.enemyCard meleeAttackType:action.meleeAttackType];
                
                if ([action.cardInAction allowAction:tempAction allLocations:unitLayout]) {
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

- (NSArray *)createBattlePlanForCard:(Card *)card friendlyUnits:(NSArray*)friendlyUnits enemyUnits:(NSArray *)enemyUnits unitLayout:(NSDictionary *)unitLayout {
    
    if (![card isOwnedByMe]) return [NSArray array];
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSUInteger remainingActionCount = [GameManager sharedManager].currentGame.numberOfAvailableActions;
    
    if ([card canPerformActionOfType:kActionTypeMove withRemainingActionCount:remainingActionCount]) {
        _moveActions = [pathFinder getMoveActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits allLocations:unitLayout];
    }
    
    if ([card canPerformActionOfType:kActionTypeMelee withRemainingActionCount:remainingActionCount]) {
        _meleeActions = [pathFinder getMeleeAttackActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits allLocations:unitLayout];
    }

    if ([card canPerformActionOfType:kActionTypeRanged withRemainingActionCount:remainingActionCount]) {
        _rangeActions = [pathFinder getRangedAttackActionsFromLocation:card.cardLocation forCard:card enemyUnits:enemyUnits allLocations:unitLayout];
    }
    
    if ([card canPerformActionOfType:kActionTypeAbility withRemainingActionCount:remainingActionCount]) {
        _abilityActions = [pathFinder getAbilityActionsFromLocation:card.cardLocation forCard:card friendlyUnits:friendlyUnits enemyUnits:enemyUnits allLocations:unitLayout];
    }
    
    return [[[_moveActions arrayByAddingObjectsFromArray:_meleeActions] arrayByAddingObjectsFromArray:_rangeActions] arrayByAddingObjectsFromArray:_abilityActions];
}

- (BOOL)hasActions {
    
    return _moveActions.count > 0 ||
    _meleeActions.count > 0 ||
    _rangeActions.count > 0 ||
    _abilityActions.count > 0;
}

@end
