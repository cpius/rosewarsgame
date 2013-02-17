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

@interface PathFinder : NSObject {
    
    NSMutableArray *_openSteps;
    NSMutableArray *_closedSteps;
}

- (NSArray *)getPathFromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation usingStrategy:(id<PathFinderStrategy>)strategy allLocations:(NSDictionary*)allLocations;

- (NSArray*)getMovableLocationsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;
- (NSArray*)getMeleeAttackableLocationsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;
- (NSArray*)getRangeAttackableLocationsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits allLocations:(NSDictionary*)allLocations;

@end
