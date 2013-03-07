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

@implementation BattlePlan

- init {
    
    self = [super init];
    
    if (self) {
        
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

- (NSDictionary *)getAttackDirectionsForCard:(Card *)card whenAttackingEnemyCard:(Card*)enemyCard withUnitLayout:(NSDictionary*)unitLayout {
    
    NSMutableDictionary *attackDirections = [NSMutableDictionary dictionary];
    
    NSArray *surroundingLocations = [enemyCard.cardLocation surroundingGridLocations];
    
    for (Action *moveAction in _moveActions) {
        
        GridLocation *attackDirection = [moveAction getLastLocationInPath];
        
        if ([surroundingLocations containsObject:attackDirection]) {
            Card *cardInLocation = [unitLayout objectForKey:attackDirection];
            
            // Use path from moveaction
            NSMutableArray *newPath = [NSMutableArray arrayWithArray:moveAction.path];
            // And add last step from enemy unit
            [newPath addObject:[[PathFinderStep alloc] initWithLocation:enemyCard.cardLocation]];
            
            if (cardInLocation == nil && [card allowPath:newPath forActionType:kActionTypeMelee allLocations:unitLayout]) {
                [attackDirections setObject:newPath forKey:attackDirection];
            }
        }
    }
    
    return attackDirections;
}

- (Action*)getActionToGridLocation:(GridLocation*)gridLocation {
    
    Action *foundAction = nil;
    
    for (Action *moveAction in _moveActions) {
        if ([[moveAction getLastLocationInPath] isEqual:gridLocation]) {
            foundAction = moveAction;
            break;
        }
    }
    
    for (Action *meleeAction in _meleeActions) {
        if ([[meleeAction getLastLocationInPath] isEqual:gridLocation]) {
            foundAction = meleeAction;
            break;
        }
    }
    
    for (Action *rangeAction in _rangeActions) {
        if ([[rangeAction getLastLocationInPath] isEqual:gridLocation]) {
            foundAction = rangeAction;
            break;
        }
    }
    
    return foundAction;
}

- (NSArray *)createBattlePlanForCard:(Card *)card enemyUnits:(NSArray *)enemyUnits unitLayout:(NSDictionary *)unitLayout {
    
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
    
    return [[_moveActions arrayByAddingObjectsFromArray:_meleeActions] arrayByAddingObjectsFromArray:_rangeActions];
}

@end
