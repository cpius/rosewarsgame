//
//  AttackPathFinderStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/15/13.
//
//

#import "MeleeAttackPathFinderStrategy.h"
#import "Card.h"

@implementation MeleeAttackPathFinderStrategy

+ (id)strategy {
    
    return [[MeleeAttackPathFinderStrategy alloc] init];
}

- (NSArray*)getReachableLocationsFromLocation:(GridLocation*)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations {
    
    Card *targetCard = [allLocations objectForKey:targetLocation];

    NSMutableArray *adjacentLocations = [NSMutableArray array];
    NSArray *surroundingGridLocations = [fromLocation surroundingGridLocations];
    
    for (GridLocation *gridLocation in surroundingGridLocations) {

        if ([self isGrindLocationInsideGameBoard:gridLocation]) {
            Card *card = [allLocations objectForKey:gridLocation];
            
            if (card == nil || card == targetCard) {
                [adjacentLocations addObject:gridLocation];
            }
        }
    }

    return [NSArray arrayWithArray:adjacentLocations];
}

@end
