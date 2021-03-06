//
//  ShortestPathStep.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import "PathFinderStep.h"

@implementation PathFinderStep

@synthesize location;
@synthesize gScore;
@synthesize hScore;
@synthesize parent;

- (id)initWithLocation:(GridLocation*)loc
{
	if ((self = [super init])) {
		location = loc;
		gScore = 0;
		hScore = 0;
		parent = nil;
	}
    
	return self;
}

- (NSString *)description
{
	return [NSString stringWithFormat:@"%@  pos=[Column %lu; Row %lu]  g=%d  h=%d  f=%d", [super description], (unsigned long)self.location.column, (unsigned long)self.location.row, self.gScore, self.hScore, [self fScore]];
}

- (BOOL)isEqual:(PathFinderStep *)other
{
	return [self.location isEqual:other.location];
}

- (int)fScore
{
	return self.gScore + self.hScore;
}
@end
