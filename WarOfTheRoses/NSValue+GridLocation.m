//
//  NSValue+GridLocation.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import "NSValue+GridLocation.h"

@implementation NSValue (GridLocation)

+ (NSValue*)valueWithGridLocation:(GridLocation)gridLocation {
    
    return [NSValue valueWithBytes:&gridLocation objCType:@encode(GridLocation)];
}

- (GridLocation)gridLocationValue {
    
    GridLocation location;
    
    [self getValue:&location];
    
    return location;
}

@end
