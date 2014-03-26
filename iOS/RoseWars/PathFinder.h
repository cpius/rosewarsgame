//
//  ShortestPath.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import <Foundation/Foundation.h>
#import "PathFinderStep.h"
#import "PathFinderStrategy.h"
#import "Card.h"

@class MeleeAttackAction;
@class RangedAttackAction;
@class MoveAction;
@interface PathFinder : NSObject {
    
    NSMutableArray *_openSteps;
    NSMutableArray *_closedSteps;
}

- (NSArray *)getPathForCard:(Card*)card fromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation usingStrategy:(id<PathFinderStrategy>)strategy allLocations:(NSDictionary *)allLocations;

- (MoveAction*)getMoveActionFromLocation:(GridLocation*)fromLocation forCard:(Card*)card toLocation:(GridLocation*)toLocation enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;
- (NSArray*)getMoveActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;

- (MeleeAttackAction*)getMeleeAttackActionForCard:(Card*)card againstEnemyUnit:(Card*)enemyUnit allLocations:(NSDictionary*)allLocations;
- (NSArray*)getMeleeAttackActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;

- (RangedAttackAction*)getRangedAttackActionForCard:(Card*)card againstEnemyUnit:(Card*)enemyUnit allLocations:(NSDictionary*)allLocations;
- (NSArray*)getRangedAttackActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;

- (NSArray*)getAbilityActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card friendlyUnits:(NSArray*)friendlyUnits enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;

@end
