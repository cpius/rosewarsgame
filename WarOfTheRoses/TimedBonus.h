//
//  FinalBonus.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

@class RangeAttribute;
@interface TimedBonus : NSObject {
    
    RangeAttribute *_parent;
    
    NSUInteger bonusValueStartedInRound;
}

@property (nonatomic, readonly) NSUInteger bonusValue;
@property (nonatomic, readonly) NSUInteger numberOfRounds;

- (id)initWithValue:(NSUInteger)bonusValue;
- (id)initWithValue:(NSUInteger)bonusValue forNumberOfRounds:(NSUInteger)numberOfRounds;

@end
