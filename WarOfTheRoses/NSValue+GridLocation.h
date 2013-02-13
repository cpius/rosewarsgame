//
//  NSValue+GridLocation.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import <Foundation/Foundation.h>

@interface NSValue (GridLocation)

+ (NSValue*)valueWithGridLocation:(GridLocation)gridLocation;
- (GridLocation)gridLocationValue;

@end
