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

@synthesize delegate = _delegate;
@synthesize friendlyAbility = _friendlyAbility;
@synthesize card = _card;

- (id)initOnCard:(Card *)card {
    
    return [self initForNumberOfRounds:1 onCard:card];
}

- (id)initForNumberOfRounds:(NSUInteger)numberOfRounds onCard:(Card*)card {
    
    self = [super init];
    
    if (self) {
        _numberOfRounds = numberOfRounds;
        _card = card;
        
        [[GameManager sharedManager].currentGame addObserver:self forKeyPath:@"currentRound" options:NSKeyValueObservingOptionNew context:nil];
        
        if ([_delegate respondsToSelector:@selector(timedAbilityWillStart:)]) {
            [_delegate timedAbilityWillStart:self];
        }
        
        [self startTimedAbility];

        if ([_delegate respondsToSelector:@selector(timedAbilityDidStart:)]) {
            [_delegate timedAbilityDidStart:self];
        }
    }
    
    return self;
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if (object == [GameManager sharedManager].currentGame && [keyPath isEqualToString:@"currentRound"]) {
        
        if ([GameManager sharedManager].currentGame.currentRound == _abilityStartedInRound + _numberOfRounds) {
            
            if ([_delegate respondsToSelector:@selector(timedAbilityWillStop:)]) {
                [_delegate timedAbilityWillStop:self];
            }

            [self stopTimedAbility];
            
            if ([_delegate respondsToSelector:@selector(timedAbilityDidStop:)]) {
                [_delegate timedAbilityDidStop:self];
            }

            [[GameManager sharedManager].currentGame removeObserver:self forKeyPath:@"currentRound"];
        }
    }
}

- (void)startTimedAbility {
    
    _abilityStartedInRound = [GameManager sharedManager].currentGame.currentRound;
}

- (void)stopTimedAbility {
    
}

@end
