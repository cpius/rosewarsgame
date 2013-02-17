//
//  BasePathFinderStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "BasePathFinderStrategy.h"

@implementation BasePathFinderStrategy

- (NSArray *)getReachableLocationsFromLocation:(GridLocation *)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations {
    
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

@end
