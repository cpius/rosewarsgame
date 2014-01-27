//
//  PathFinderStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/15/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@protocol PathFinderStrategy <NSObject>

- (NSArray*)getReachableLocationsForCard:(Card*)card fromLocation:(GridLocation*)fromLocation targetLocation:(GridLocation*)targetLocation allLocations:(NSDictionary *)allLocations;

@end
