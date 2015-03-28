//
//  FixedDiceStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import "FixedDiceStrategy.h"

@implementation FixedDiceStrategy

@synthesize fixedDieValue;

+ (id)strategyWithFixedValue:(NSUInteger)fixedValue {
    
    FixedDiceStrategy *strategy = [[FixedDiceStrategy alloc] init];
    strategy.fixedDieValue = fixedValue;
    
    return strategy;
}

+ (id)strategy {
    
    return [[FixedDiceStrategy alloc] init];
}

- (NSUInteger)rollDiceWithDie:(NSUInteger)die {
    
    return fixedDieValue;
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"Fixed dice: %lu", (unsigned long)fixedDieValue];
}

@end
