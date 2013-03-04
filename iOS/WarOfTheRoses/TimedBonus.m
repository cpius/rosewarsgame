//
//  FinalBonus.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "TimedBonus.h"
#import "RangeAttribute.h"
#import "GameManager.h"

@implementation TimedBonus

@synthesize bonusValue = _bonusValue;
@synthesize numberOfRounds = _numberOfRounds;

- (id)initWithValue:(NSUInteger)bonusValue {
    
    return [self initWithValue:bonusValue forNumberOfRounds:1];
}

- (id)initWithValue:(NSUInteger)bonusValue forNumberOfRounds:(NSUInteger)numberOfRounds {
    
    self = [super init];
    
    if (self) {
        _bonusValue = bonusValue;
        _numberOfRounds = numberOfRounds;
        
        [[GameManager sharedManager].currentGame addObserver:self forKeyPath:@"currentRound" options:NSKeyValueObservingOptionNew context:nil];
    }
    
    return self;
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if (object == [GameManager sharedManager].currentGame && [keyPath isEqualToString:@"currentRound"]) {
        
        if ([GameManager sharedManager].currentGame.currentRound == bonusValueStartedInRound + _numberOfRounds) {
            [self stopTimedBonus];
            [[GameManager sharedManager].currentGame removeObserver:self forKeyPath:@"currentRound"];
        }
    }
}

- (void)startTimedBonus:(RangeAttribute*)parent {
    
    _parent = parent;
    bonusValueStartedInRound = [GameManager sharedManager].currentGame.currentRound;
}

- (void)stopTimedBonus {
    
    [_parent removeTimedBonus:self];
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"Bonus value %d for %d rounds", _bonusValue, _numberOfRounds];
}

@end
