//
//  ShortestPath.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import "PathFinder.h"
#import "MovePathFinderStrategy.h"
#import "MeleeAttackPathFinderStrategy.h"
#import "RangedAttackPathFinderStrategy.h"

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

- (NSArray *)getPathFromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation usingStrategy:(id<PathFinderStrategy>)strategy allLocations:(NSDictionary *)allLocations {
        
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
            
            return [NSArray arrayWithArray:path];
        }
        
        NSArray *adjacentGridLocations = [strategy getReachableLocationsFromLocation:currentStep.location targetLocation:toLocation allLocations:allLocations];
        
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

- (NSArray*)getMovableLocationsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSMutableArray *movableLocations = [NSMutableArray array];
    
    for (int row = 1; row <= BOARDSIZE_ROWS; row++) {
        for (int column = 1; column <= BOARDSIZE_COLUMNS; column++) {
        
            GridLocation *toLocation = [GridLocation gridLocationWithRow:row column:column];
            NSArray *path = [self getPathFromGridLocation:fromLocation toGridLocation:toLocation usingStrategy:[MovePathFinderStrategy strategy] allLocations:allLocations];
            
            if (path != nil && path.count <= card.move + 1) {
                [movableLocations addObject:toLocation];
            }
        }
    }
    
    return [NSArray arrayWithArray:movableLocations];
}

- (NSArray*)getMeleeAttackableLocationsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSMutableArray *attackableLocations = [NSMutableArray array];
    
    for (Card *enemyCard in enemyUnits) {
        
        GridLocation *enemyLocation = enemyCard.cardLocation;
        
        NSArray *path = [self getPathFromGridLocation:fromLocation toGridLocation:enemyLocation usingStrategy:[MeleeAttackPathFinderStrategy strategy] allLocations:allLocations];
        
        if (path != nil) {
            if (path.count <= card.move + 1) {
                [attackableLocations addObject:enemyLocation];
            }
        }
    }
    
    return [NSArray arrayWithArray:attackableLocations];
}

- (NSArray *)getRangeAttackableLocationsFromLocation:(GridLocation *)fromLocation forCard:(Card *)card enemyUnits:(NSArray *)enemyUnits allLocations:(NSDictionary *)allLocations {
    
    NSMutableArray *attackableLocations = [NSMutableArray array];
    
    for (Card *enemyCard in enemyUnits) {
        
        GridLocation *enemyLocation = enemyCard.cardLocation;
        
        NSArray *path = [self getPathFromGridLocation:fromLocation toGridLocation:enemyLocation usingStrategy:[RangedAttackPathFinderStrategy strategy] allLocations:allLocations];
        
        if (path != nil) {
            if (path.count <= card.range + 1) {
                [attackableLocations addObject:enemyLocation];
            }
        }
    }
    
    return [NSArray arrayWithArray:attackableLocations];
}

@end
