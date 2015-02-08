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
#import "AbilityAction.h"

@interface PathFinder()

@property (nonatomic, readonly) GameManager *gamemanager;

- (void)insertInOpenSteps:(PathFinderStep*)step;
- (int)computeHScoreFromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation;
- (int)costToMovingFromStep:(PathFinderStep*)step toAdjacentStep:(PathFinderStep*)toStep;

- (PathFinderStep*)getStepWithLowestFCost;
- (void)removeStepWithLowestFCost;
- (BOOL)isStep:(PathFinderStep*)step presentInList:(NSArray*)list;
- (PathFinderStep*)getStepWithLocation:(GridLocation*)location fromList:(NSArray*)list;

@end

@implementation PathFinder

- (instancetype)init {
    NSAssert(YES, @"use initWithGameManager");
    return nil;
}

- (instancetype)initWithGameManager:(GameManager*)gamemanager
{
    self = [super init];
    if (self) {
        _gamemanager = gamemanager;
    }
    return self;
}

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
    
    return abs((int)toLocation.column - (int)fromLocation.column) + abs((int)toLocation.row - (int)fromLocation.row);
}

- (int)costToMovingFromStep:(PathFinderStep *)step toAdjacentStep:(PathFinderStep *)toStep {
    // The further away from the destination, the more expensive
    return [self computeHScoreFromGridLocation:step.location toGridLocation:toStep.location];
    //return 1;
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

- (MoveAction*)getMoveActionFromLocation:(GridLocation*)fromLocation forCard:(Card*)card toLocation:(GridLocation*)toLocation enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSArray *path = [self getPathForCard:card fromGridLocation:fromLocation toGridLocation:toLocation usingStrategy:[PathFinderStrategyFactory getMoveStrategy] allLocations:allLocations];
    
    MoveAction *action = [[MoveAction alloc] initWithGameManager:self.gamemanager path:path andCardInAction:card enemyCard:nil];
    
    if ([card allowAction:action allLocations:allLocations]) {
        return action;
    }
    
    return nil;
}


- (NSArray*)getMoveActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSMutableArray *moveActions = [NSMutableArray array];
    
    for (int row = 1; row <= BOARDSIZE_ROWS; row++) {
        for (int column = 1; column <= BOARDSIZE_COLUMNS; column++) {
        
            GridLocation *toLocation = [GridLocation gridLocationWithRow:row column:column];
            
            MoveAction *moveaction = [self getMoveActionFromLocation:fromLocation forCard:card toLocation:toLocation enemyUnits:enemyUnits allLocations:allLocations];
            
            if (moveaction != nil) {
                [moveActions addObject:moveaction];
            }
        }
    }
    
    return [NSArray arrayWithArray:moveActions];
}

- (MeleeAttackAction *)getMeleeAttackActionForCard:(Card *)card againstEnemyUnit:(Card *)enemyUnit allLocations:(NSDictionary *)allLocations {
    
    if (enemyUnit.dead) return nil;
    
    GridLocation *enemyLocation = enemyUnit.cardLocation;
    
    NSArray *path = [self getPathForCard:card fromGridLocation:card.cardLocation toGridLocation:enemyLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackWithConquerStrategy] allLocations:allLocations];
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:path andCardInAction:card enemyCard:enemyUnit meleeAttackType:kMeleeAttackTypeConquer];
    
    if ([card allowAction:meleeAction allLocations:allLocations]) {
        return meleeAction;
    }
    else {
        
        NSUInteger meleeRange = [card.cardLocation dictanceToGridLocation:enemyLocation];
        
        if (meleeRange <= card.meleeRange) {
            path = [self getPathForCard:card fromGridLocation:card.cardLocation toGridLocation:enemyLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:allLocations];
            
            meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:path andCardInAction:card enemyCard:enemyUnit meleeAttackType:kMeleeAttackTypeNormal];
            
            if ([card allowAction:meleeAction allLocations:allLocations]) {
                return meleeAction;
            }
        }
    }
    
    return nil;
}

- (NSArray*)getMeleeAttackActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations {
    
    NSMutableArray *attackActions = [NSMutableArray array];
    
    for (Card *enemyCard in enemyUnits) {
        
        MeleeAttackAction *action = [self getMeleeAttackActionForCard:card againstEnemyUnit:enemyCard allLocations:allLocations];
        
        if (action != nil) {
            [attackActions addObject:action];
        }
    }
    
    return [NSArray arrayWithArray:attackActions];
}

- (RangedAttackAction*)getRangedAttackActionForCard:(Card*)card againstEnemyUnit:(Card*)enemyUnit allLocations:(NSDictionary*)allLocations {
    
    NSArray *path = [self getPathForCard:card fromGridLocation:card.cardLocation toGridLocation:enemyUnit.cardLocation usingStrategy:[PathFinderStrategyFactory getRangedAttackStrategy] allLocations:allLocations];
    
    RangedAttackAction *action = [[RangedAttackAction alloc] initWithGameManager:self.gamemanager path:path andCardInAction:card enemyCard:enemyUnit];
    
    if ([card allowAction:action allLocations:allLocations]) {
        return action;
    }
    
    return nil;
}

- (NSArray *)getRangedAttackActionsFromLocation:(GridLocation *)fromLocation forCard:(Card *)card enemyUnits:(NSArray *)enemyUnits allLocations:(NSDictionary *)allLocations {
    
    NSMutableArray *attackActions = [NSMutableArray array];
    
    for (Card *enemyCard in enemyUnits) {
        
        if (enemyCard.dead) continue;
        
        Action *action = [self getRangedAttackActionForCard:card againstEnemyUnit:enemyCard allLocations:allLocations];
        
        if (action) {
            [attackActions addObject:action];
        }
    }
    
    return [NSArray arrayWithArray:attackActions];
}

- (NSArray *)getAbilityActionsFromLocation:(GridLocation *)fromLocation forCard:(Card *)card friendlyUnits:(NSArray*)friendlyUnits enemyUnits:(NSArray *)enemyUnits allLocations:(NSDictionary *)allLocations {
    
    NSMutableArray *abilityActions = [NSMutableArray array];
    NSArray *allUnits = allLocations.allValues;
    
    for (Card *targetCard in allUnits) {
        
        if (targetCard.dead) continue;
        
        GridLocation *targetLocation = targetCard.cardLocation;
        
        NSArray *path = [self getPathForCard:card fromGridLocation:fromLocation toGridLocation:targetLocation usingStrategy:[PathFinderStrategyFactory getRangedAttackStrategy] allLocations:allLocations];
        
        Action *action = [[AbilityAction alloc] initWithGameManager:self.gamemanager path:path andCardInAction:card targetCard:targetCard];
        
        if ([card allowAction:action allLocations:allLocations] && [card isValidTarget:targetCard]) {
            [abilityActions addObject:action];
        }
    }
    
    return [NSArray arrayWithArray:abilityActions];
}

@end
