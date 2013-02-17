//
//  PathFinderStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/15/13.
//
//

#import <Foundation/Foundation.h>

@protocol PathFinderStrategy <NSObject>

- (NSArray*)getReachableLocationsFromLocation:(GridLocation*)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations;

@end
