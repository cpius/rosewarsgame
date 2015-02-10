//
//  FinalBonus.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 12/27/12.
//
//

#import "TimedBonus.h"
#import "HKAttribute.h"
#import "GameManager.h"

@interface TimedBonus()

@property (nonatomic, assign) BOOL observerAdded;

@end

@implementation TimedBonus

@synthesize bonusValue = _bonusValue;

- (id)initWithValue:(NSUInteger)bonusValue gamemanager:(GameManager*)gamemanager {
    
    return [self initWithValue:bonusValue forNumberOfTurns:2 gamemanager:gamemanager];
}

- (id)initWithValue:(NSUInteger)bonusValue forNumberOfTurns:(NSUInteger)numberOfTurns gamemanager:(GameManager*)gamemanager {
    
    self = [super init];
    
    if (self) {
        _gamemanager = gamemanager;
        _bonusValue = bonusValue;
        _numberOfTurns = numberOfTurns;
        
        [_gamemanager.currentGame addObserver:self forKeyPath:@"turnCounter" options:NSKeyValueObservingOptionNew context:nil];
        self.observerAdded = YES;
    }
    
    return self;
}

- (void)dealloc {
    if (self.observerAdded) {
        [self.gamemanager.currentGame removeObserver:self forKeyPath:@"turnCounter"];
    }
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if (object == self.gamemanager.currentGame && [keyPath isEqualToString:@"turnCounter"]) {
        
        if (self.gamemanager.currentGame.turnCounter == bonusValueStartedInTurn + _numberOfTurns) {
            [self stopTimedBonus];
            @try {
                if (self.observerAdded) {
                    [self.gamemanager.currentGame removeObserver:self forKeyPath:@"turnCounter"];
                    self.observerAdded = NO;
                }
            }@catch (NSException *exception) {}
        }
    }
}

- (void)startTimedBonus:(HKAttribute*)parent {
    _parent = parent;
    bonusValueStartedInTurn = self.gamemanager.currentGame.turnCounter;
}

- (void)stopTimedBonus {
    
    [_parent removeTimedBonus:self];
}

- (NSString *)description {
    
    return [NSString stringWithFormat:@"Bonus value %lu for %lu turns", (unsigned long)_bonusValue, (unsigned long)_numberOfTurns];
}

@end
