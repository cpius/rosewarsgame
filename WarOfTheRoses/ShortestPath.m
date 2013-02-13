//
//  ShortestPath.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import "ShortestPath.h"

@interface ShortestPath()

- (void)insertInOpenSteps:(ShortestPathStep*)step;
- (int)computeHScoreFromGridLocation:(GridLocation)fromLocation toGridLocation:(GridLocation)toLocation;
- (int)costToMovingFromStep:(ShortestPathStep*)step toAdjacentStep:(ShortestPathStep*)toStep;

- (ShortestPathStep*)getStepWithLowestFCost;
- (void)removeStepWithLowestFCost;
- (BOOL)isStep:(ShortestPathStep*)step presentInList:(NSArray*)list;
- (ShortestPathStep*)getStepWithLocation:(GridLocation)location fromList:(NSArray*)list;

@end

@implementation ShortestPath

@synthesize datasource = _datasource;

- (void)insertInOpenSteps:(ShortestPathStep *)step {
    
    int stepfScore = step.fScore;
    int openStepsCount = _openSteps.count;
    
    if (openStepsCount == 0) {
        [_openSteps insertObject:step atIndex:0];
    }
    else {
        for (int i = 0; i < openStepsCount; i++) {
            
            ShortestPathStep * stepFromOpenList = [_openSteps objectAtIndex:i];
            if (stepfScore <= stepFromOpenList.fScore) {
                
                [_openSteps insertObject:step atIndex:i];
                break;
            }
        }
    }
}

- (int)computeHScoreFromGridLocation:(GridLocation)fromLocation toGridLocation:(GridLocation)toLocation {
    
    return abs(toLocation.column - fromLocation.column) + abs(toLocation.row - fromLocation.row);
}

- (int)costToMovingFromStep:(ShortestPathStep *)step toAdjacentStep:(ShortestPathStep *)toStep {
    
    return 1;
}

- (ShortestPathStep *)getStepWithLowestFCost {
    
    return [_openSteps objectAtIndex:0];
}

- (void)removeStepWithLowestFCost {
    
    [_openSteps removeObject:[self getStepWithLowestFCost]];
}

- (BOOL)isStep:(ShortestPathStep *)step presentInList:(NSArray *)list {
    
    GridLocation location = step.location;
    
    for (ShortestPathStep *pathStep in list) {
        if (GridLocationEqualToLocation(location, pathStep.location)) {
            return YES;
        }
    }
    
    return NO;
}

- (ShortestPathStep *)getStepWithLocation:(GridLocation)location fromList:(NSArray *)list {
    
    for (ShortestPathStep *step in list) {
        if (GridLocationEqualToLocation(location, step.location)) {
            return step;
        }
    }
    
    return nil;
}

- (NSArray *)getPathFromGridLocation:(GridLocation)fromLocation toGridLocation:(GridLocation)toLocation {
    
    if (_datasource == nil) {
        CCLOG(@"Datasource must be set before pathfinding");
        return nil;
    }
    
    BOOL pathFound = NO;
    
    NSMutableArray *path = [[NSMutableArray alloc] init];
    
    _openSteps = [[NSMutableArray alloc] init];
    _closedSteps = [[NSMutableArray alloc] init];
    
    [self insertInOpenSteps:[[ShortestPathStep alloc] initWithLocation:fromLocation]];
    
    do {
        
        ShortestPathStep *currentStep = [self getStepWithLowestFCost];
        
        [path addObject:currentStep];
        [_closedSteps addObject:currentStep];
        [self removeStepWithLowestFCost];
        
        if (GridLocationEqualToLocation(currentStep.location, toLocation)) {
            
            pathFound = YES;
            
            return [NSArray arrayWithArray:path];
        }
        
        NSArray *adjacentGridLocations = [_datasource requestAdjacentGridLocationsForGridLocation:currentStep.location withTargetLocation:toLocation];
        
        for (NSValue *value in adjacentGridLocations) {
            
            ShortestPathStep *step = [[ShortestPathStep alloc] initWithLocation:[value gridLocationValue]];
            
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

- (NSArray *)getReachableLocationsFromLocation:(GridLocation)fromLocation withMaxRange:(NSUInteger)maxRange {
    
    return nil;
}

@end
