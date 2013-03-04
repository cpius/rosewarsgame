//
//  FinalBonus.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//
#import "BaseBonus.h"

@class RangeAttribute;
@interface TimedBonus : BaseBonus {
    
    RangeAttribute *_parent;
    
    NSUInteger bonusValueStartedInRound;
}

@property (nonatomic, readonly) NSUInteger numberOfRounds;

- (id)initWithValue:(NSUInteger)bonusValue;
- (id)initWithValue:(NSUInteger)bonusValue forNumberOfRounds:(NSUInteger)numberOfRounds;

- (void)startTimedBonus:(RangeAttribute*)parent;

@end
