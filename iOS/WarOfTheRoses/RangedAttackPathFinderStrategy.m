//
//  RangedAttackPathFinderStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/17/13.
//
//

#import "RangedAttackPathFinderStrategy.h"

@implementation RangedAttackPathFinderStrategy

+ (id)strategy {
    
    return [[RangedAttackPathFinderStrategy alloc] init];
}

- (NSArray*)getReachableLocationsForCard:(Card*)card fromLocation:(GridLocation*)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations {
    
    NSMutableArray *adjacentLocations = [NSMutableArray array];
    NSArray *surroundingGridLocations = [fromLocation surroundingGridLocations];
    
    for (GridLocation *gridLocation in surroundingGridLocations) {
        
        if ([self isGrindLocationInsideGameBoard:gridLocation]) {
            [adjacentLocations addObject:gridLocation];
        }
    }

    return [NSArray arrayWithArray:adjacentLocations];
}

@end
