//
//  ShortestPath.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import "PathFinder.h"
#import "PathFinderStrategyFactory.h"
#import "MoveAction.h"
#import "MeleeAttackAction.h"
#import "RangedAttackAction.h"

@interface PathFinder()

- (void)insertInOpenSteps:(PathFinderStep*)step;
- (int)computeHScoreFromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation;
- (int)costToMovingFromStep:(PathFinderStep*)step toAdjacentStep:(PathFinderStep*)toStep;

- (PathFinderStep*)getStepWithLowestFCost;
- (void)removeStepWithLowestFCost;
- (BOOL)isStep:(PathFinderStep*)step presentInList:(NSArray*)list;
- (PathFinderStep*)getStepWithLocation:(GridLocation*)location fromList:(NSArray*)list;

@end

@implementation PathFinder

- (void)insertInOpenSteps:(PathFinderStep *)step {
    
    int stepfScore = step.fScore;
    int openStepsCount = _openSteps.count;
    
    if (openStepsCount == 0) {
        [_openSteps insertObject:step atIndex:0];
    }
    else {
        for (int i = 0; i < openStepsCount; i++) {
            
            PathFinderStep * stepFromOpenList = [_openSteps objectAtIndex:i];
            if (stepfScore <= stepFromOpenList.fScore) {
                
                [_openSteps insertObject:step atIndex:i];
                break;
            }
        }
    }
}

- (int)computeHScoreFromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation {
    
    return abs(toLocation.column - fromLocation.column) + abs(toLocation.row - fromLocation.row);
}

- (int)costToMovingFromStep:(PathFinderStep *)step toAdjacentStep:(PathFinderStep *)toStep {
    
    return 1;
}

- (PathFinderStep *)getStepWithLowestFCost {
    
    return [_openSteps objectAtIndex:0];
}

- (void)removeStepWithLowestFCost {
    
    [_openSteps removeObject:[self getStepWithLowestFCost]];
}

- (BOOL)isStep:(PathFinderStep *)step presentInList:(NSArray *)list {
    
    GridLocation *location = step.location;
    
    for (PathFinderStep *pathStep in list) {
        if ([location isEqual:pathStep.location]) {
            return YES;
        }
    }
    
    return NO;
}

- (PathFinderStep *)getStepWithLocation:(GridLocation*)location fromList:(NSArray *)list {
    
    for (PathFinderStep *pathStep in list) {
        if ([location isEqual:pathStep.location]) {
            return pathStep;
        }
    }
    
    return nil;
}

- (NSArray *)getPathForCard:(Card*)card fromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation usingStrategy:(id<PathFinderStrategy>)strategy allLocations:(NSDictionary *)allLocations {
        
    BOOL pathFound = NO;
    
    NSMutableArray *path = [[NSMutableArray alloc] init];
    
    _openSteps = [[NSMutableArray alloc] init];
    _closedSteps = [[NSMutableArray alloc] init];
    
    [self insertInOpenSteps:[[PathFinderStep alloc] initWithLocation:fromLocation]];
    
    do {
        
        PathFinderStep *currentStep = [self getStepWithLowestFCost];
        
        [path addObject:currentStep];
        [_closedSteps addObject:currentStep];
        [self removeStepWithLowestFCost];
        
        if ([currentStep.location isEqual:toLocation]) {
            
            pathFound = YES;
            
            [path removeObjectAtIndex:0];
            return [NSArray arrayWithArray:path];
        }
        
        NSArray *adjacentGridLocations = [strategy getReachableLocationsForCard:card fromLocation:currentStep.location targetLocation:toLocation allLocations:allLocations];
        
        for (GridLocation *location in adjacentGridLocations) {
            
            PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:location];
            
            if ([self isStep:step presentInList:_closedSteps]) {
                continue;
            }
            
            int moveCost = [self costToMovingFromStep:currentStep toAdjacentStep:step];
            
            if (![self isStep:step presentInList:_openSteps]) {
                
                step.parent = currentStep;
                step.gScore = currentStep.gScore + moveCost;
                step.hScore = [self computeHScoreFromGridLocation:step.location toGridLocation:toLocation];
                
                [self insertInOpenSteps:step];
            }
            else {
                
                step = [self getStepWithLocation:step.location fromList:_openSteps];
                
                if ((currentStep.gScore + moveCost) < step.gScore) {
                    step.gScore = currentStep.gScore + moveCost;
                    
                    // Remove and add step to reorder according to f value
                    [_openSteps removeObject:step];
                    [self insertInOpenSteps:step];
                }
            }
        }
        
    } while (_openSteps.count > 0);
    
    // No path found
    return nil;
}

- (NSArray*)getMoveActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSMutableArray *moveActions = [NSMutableArray array];
    
    for (int row = 1; row <= BOARDSIZE_ROWS; row++) {
        for (int column = 1; column <= BOARDSIZE_COLUMNS; column++) {
        
            GridLocation *toLocation = [GridLocation gridLocationWithRow:row column:column];
            NSArray *path = [self getPathForCard:card fromGridLocation:fromLocation toGridLocation:toLocation usingStrategy:[PathFinderStrategyFactory getMoveStrategy] allLocations:allLocations];
            
            if ([card allowPath:path forActionType:kActionTypeMove allLocations:allLocations]) {
                [moveActions addObject:[[MoveAction alloc] initWithPath:path andCardInAction:card enemyCard:nil]];
            }
        }
    }
    
    return [NSArray arrayWithArray:moveActions];
}

- (NSArray*)getMeleeAttackActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSMutableArray *attackActions = [NSMutableArray array];
    
    for (Card *enemyCard in enemyUnits) {
        
        if (enemyCard.dead) continue;

        GridLocation *enemyLocation = enemyCard.cardLocation;
        
        NSArray *path = [self getPathForCard:card fromGridLocation:fromLocation toGridLocation:enemyLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:allLocations];
        
        if ([card allowPath:path forActionType:kActionTypeMelee allLocations:allLocations]) {
            [attackActions addObject:[[MeleeAttackAction alloc] initWithPath:path andCardInAction:card enemyCard:enemyCard]];
        }
    }
    
    return [NSArray arrayWithArray:attackActions];
}

- (NSArray *)getRangedAttackActionsFromLocation:(GridLocation *)fromLocation forCard:(Card *)card enemyUnits:(NSArray *)enemyUnits allLocations:(NSDictionary *)allLocations {
    
    NSMutableArray *attackActions = [NSMutableArray array];
    
    for (Card *enemyCard in enemyUnits) {
        
        if (enemyCard.dead) continue;
        
        GridLocation *enemyLocation = enemyCard.cardLocation;
        
        NSArray *path = [self getPathForCard:card fromGridLocation:fromLocation toGridLocation:enemyLocation usingStrategy:[PathFinderStrategyFactory getRangedAttackStrategy] allLocations:allLocations];
        
        if ([card allowPath:path forActionType:kActionTypeRanged allLocations:allLocations]) {
            [attackActions addObject:[[RangedAttackAction alloc] initWithPath:path andCardInAction:card enemyCard:enemyCard]];
        }
    }
    
    return [NSArray arrayWithArray:attackActions];
}

@end
