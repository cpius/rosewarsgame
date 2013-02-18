//
//  BasePathFinderStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "BasePathFinderStrategy.h"

@implementation BasePathFinderStrategy

- (NSArray *)getReachableLocationsForCard:(Card*)card fromLocation:(GridLocation *)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations {
    
    @throw [NSException exceptionWithName:@"PathFinderException" reason:@"Must be overridden in subclass" userInfo:nil];
}

- (BOOL)isGrindLocationInsideGameBoard:(GridLocation *)location {
    
    if (location.column >= 1 &&
        location.column <= BOARDSIZE_COLUMNS &&
        location.row >= 1 &&
        location.row <= BOARDSIZE_ROWS) {
        return YES;
    }
    
    return NO;
}

- (BOOL)card:(Card*)card blockedByZoneOfControlUnitWhenMovingFromLocation:(GridLocation*)fromLocation toLocation:(GridLocation*)toLocation allLocations:(NSDictionary *)allLocations {
    
    BOOL blocked = NO;
    
    if ((toLocation.column > fromLocation.column) || (toLocation.column < fromLocation.column)) {
        
        // Moving left or right - check location above and below for ZOC
        Card *cardAbove = [allLocations objectForKey:[fromLocation locationAbove]];
        Card *cardBelow = [allLocations objectForKey:[fromLocation locationBelow]];
        
        blocked = [cardAbove zoneOfControlAgainst:card] || [cardBelow zoneOfControlAgainst:card];
    }
    
    if ((toLocation.row > fromLocation.row) || (toLocation.row < fromLocation.row)) {
        
        // Moving up or down - check locations left and right
        Card *cardToTheLeft = [allLocations objectForKey:[fromLocation locationToTheLeft]];
        Card *cardToTheRight = [allLocations objectForKey:[fromLocation locationToTheRight]];
        
        blocked = [cardToTheLeft zoneOfControlAgainst:card] || [cardToTheRight zoneOfControlAgainst:card];
    }
        
    return blocked;
}

@end
