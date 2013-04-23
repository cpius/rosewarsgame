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

@interface TimedAbility()

- (void)notifyAndStopTimedAbility;

@end

@implementation TimedAbility

@synthesize delegate = _delegate;
@synthesize friendlyAbility = _friendlyAbility;
@synthesize card = _card;
@synthesize abilityType = _abilityType;
@synthesize abilityStartedInTurn = _abilityStartedInTurn;

- (id)initOnCard:(Card *)card {
    
    return [self initForNumberOfTurns:1 onCard:card];
}

- (id)initForNumberOfTurns:(NSUInteger)numberOfTurns onCard:(Card*)card {
    
    self = [super init];
    
    if (self) {
        _numberOfTurns = numberOfTurns;
        _card = card;
        
        [[GameManager sharedManager].currentGame addObserver:self forKeyPath:@"turnCounter" options:NSKeyValueObservingOptionNew context:nil];
        
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

- (id)initExistingAbilityWithAbilityData:(NSDictionary*)abilityData onCard:(Card*)card {
    
    self = [super init];
    
    if (self) {
        _numberOfTurns = [[abilityData objectForKey:@"numberofturns"] integerValue];
        _abilityStartedInTurn = [[abilityData objectForKey:@"started_in_turn"] integerValue];
        _card = card;
        
        [self fromDictionary:abilityData];
        
        [[GameManager sharedManager].currentGame addObserver:self forKeyPath:@"turnCounter" options:NSKeyValueObservingOptionNew context:nil];
        
        if (_numberOfTurns > 0) {

            if ([_delegate respondsToSelector:@selector(timedAbilityWillStart:)]) {
                [_delegate timedAbilityWillStart:self];
            }
            [self reactivateTimedAbility];
            
            if ([_delegate respondsToSelector:@selector(timedAbilityDidStart:)]) {
                [_delegate timedAbilityDidStart:self];
            }
        }
        else {
            [self stopTimedAbility];
        }
    }
    
    return self;
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    
    if (object == [GameManager sharedManager].currentGame && [keyPath isEqualToString:@"turnCounter"]) {
        
        if ([GameManager sharedManager].currentGame.turnCounter == _abilityStartedInTurn + _numberOfTurns) {
            [self notifyAndStopTimedAbility];
        }
    }
}

- (void)notifyAndStopTimedAbility {
    
    if ([_delegate respondsToSelector:@selector(timedAbilityWillStop:)]) {
        [_delegate timedAbilityWillStop:self];
    }
    
    [self stopTimedAbility];
    
    if ([_delegate respondsToSelector:@selector(timedAbilityDidStop:)]) {
        [_delegate timedAbilityDidStop:self];
    }
}

- (void)forceTurnChanged {
    
    _abilityStartedInTurn--;
    
    if ([GameManager sharedManager].currentGame.turnCounter == _abilityStartedInTurn + _numberOfTurns) {
        [self notifyAndStopTimedAbility];
    }
}

- (void)reactivateTimedAbility {
    
}

- (void)startTimedAbility {
    
    _abilityStartedInTurn = [GameManager sharedManager].currentGame.turnCounter;
}

- (void)stopTimedAbility {
    
}

- (void)applyEffect {
    
}

- (NSDictionary *)asDictionary {
    
    return [NSDictionary dictionary];
}

- (void)fromDictionary:(NSDictionary*)dictionary {
    
}

- (void)dealloc {
    
    [[GameManager sharedManager].currentGame removeObserver:self forKeyPath:@"turnCounter"];
}

@end
