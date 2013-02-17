//
//  BasePathFinderStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <Foundation/Foundation.h>
#import "PathFinderStrategy.h"
#import "GridLocation.h"
#import "GameManager.h"

@interface BasePathFinderStrategy : NSObject <PathFinderStrategy>

- (BOOL)isGrindLocationInsideGameBoard:(GridLocation*)location;

@end
