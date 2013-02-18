//
//  MovePathFinderStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/15/13.
//
//

#import "MovePathFinderStrategy.h"
#import "Card.h"

@implementation MovePathFinderStrategy

+ (id)strategy {
    
    return [[MovePathFinderStrategy alloc] init];
}

- (NSArray*)getReachableLocationsForCard:(Card*)card fromLocation:(GridLocation*)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations {
    
    NSMutableArray *adjacentLocations = [NSMutableArray array];
    
    NSArray *surroundingGridLocations = [fromLocation surroundingGridLocations];
    
    for (GridLocation *gridLocation in surroundingGridLocations) {
        
        if ([self isGrindLocationInsideGameBoard:gridLocation]) {
            Card *cardAtToLocation = [allLocations objectForKey:gridLocation];
            
            if (cardAtToLocation == nil && ![self card:card blockedByZoneOfControlUnitWhenMovingFromLocation:fromLocation toLocation:gridLocation allLocations:allLocations]) {
                
                [adjacentLocations addObject:gridLocation];
            }
        }
    }

    return [NSArray arrayWithArray:adjacentLocations];
}


@end
