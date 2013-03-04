//
//  TimedAbility.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/4/13.
//
//

#import "TimedAbility.h"
#import "Card.h"
#import "GameManager.h"

@implementation TimedAbility

- (id)initForNumberOfRounds:(NSUInteger)numberOfRounds {
    
    self = [super init];
    
    if (self) {
        _numberOfRounds = numberOfRounds;
        
        [[GameManager sharedManager].currentGame addObserver:self forKeyPath:@"currentRound" options:NSKeyValueObservingOptionNew context:nil];
    }
    
    return self;
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if (object == [GameManager sharedManager].currentGame && [keyPath isEqualToString:@"currentRound"]) {
        
        if ([GameManager sharedManager].currentGame.currentRound == _abilityStartedInRound + _numberOfRounds) {
            [self stopTimedAbility];
            [[GameManager sharedManager].currentGame removeObserver:self forKeyPath:@"currentRound"];
        }
    }
}

- (void)startTimedAbilityOnCard:(Card*)card {
    
    _card = card;
    _abilityStartedInRound = [GameManager sharedManager].currentGame.currentRound;
}

- (void)stopTimedAbility {
    
}

@end
