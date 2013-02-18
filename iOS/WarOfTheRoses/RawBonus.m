//
//  RawBonus.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "RawBonus.h"

@implementation RawBonus

@synthesize bonusValue = _bonusValue;

- (id)initWithValue:(NSUInteger)bonusValue {
    
    self = [super init];
    
    if (self) {
        _bonusValue = bonusValue;
    }
    
    return self;
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"Bonus value %d added", _bonusValue];
}
@end
