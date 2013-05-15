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
@synthesize numberOfRounds = _numberOfTurns;

- (id)initWithValue:(NSUInteger)bonusValue {
    
    return [self initWithValue:bonusValue forNumberOfTurns:2];
}

- (id)initWithValue:(NSUInteger)bonusValue forNumberOfTurns:(NSUInteger)numberOfTurns {
    
    self = [super init];
    
    if (self) {
        _bonusValue = bonusValue;
        _numberOfTurns = numberOfTurns;
        
        [[GameManager sharedManager].currentGame addObserver:self forKeyPath:@"turnCounter" options:NSKeyValueObservingOptionNew context:nil];
    }
    
    return self;
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if (object == [GameManager sharedManager].currentGame && [keyPath isEqualToString:@"turnCounter"]) {
        
        if ([GameManager sharedManager].currentGame.turnCounter == bonusValueStartedInTurn + _numberOfTurns) {
            [self stopTimedBonus];
            [[GameManager sharedManager].currentGame removeObserver:self forKeyPath:@"turnCounter"];
        }
    }
}

- (void)startTimedBonus:(RangeAttribute*)parent {
    
    _parent = parent;
    bonusValueStartedInTurn = [GameManager sharedManager].currentGame.turnCounter;
}

- (void)stopTimedBonus {
    
    [_parent removeTimedBonus:self];
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"Bonus value %d for %d turns", _bonusValue, _numberOfTurns];
}

@end
