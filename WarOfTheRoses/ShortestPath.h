//
//  ShortestPath.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import <Foundation/Foundation.h>
#import "ShortestPathStep.h"

@protocol ShortestPathDatasource <NSObject>

- (NSArray*)requestAdjacentGridLocationsForGridLocation:(GridLocation)location withTargetLocation:(GridLocation)targetLocation;

@end

@interface ShortestPath : NSObject {
    
    NSMutableArray *_openSteps;
    NSMutableArray *_closedSteps;
}

@property (nonatomic, weak) id<ShortestPathDatasource> datasource;

- (NSArray*)getPathFromGridLocation:(GridLocation)fromLocation toGridLocation:(GridLocation)toLocation;
- (NSArray*)getReachableLocationsFromLocation:(GridLocation)fromLocation withMaxMoves:(NSUInteger)maxMoves;

@end
