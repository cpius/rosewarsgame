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
#import "Action.h"

@interface TimedAbility()

- (void)notifyAndStopTimedAbility;

@property (nonatomic, assign) BOOL observerAdded;

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
        
        [_card.gamemanager.currentGame addObserver:self forKeyPath:@"turnCounter" options:NSKeyValueObservingOptionNew context:nil];
        self.observerAdded = YES;
        NSLog(@"Timed ability of type %@ ADDED to card %@", NSStringFromClass(self.class), card);
        
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
        
        [self.card.gamemanager.currentGame addObserver:self forKeyPath:@"turnCounter" options:NSKeyValueObservingOptionNew context:nil];
        NSLog(@"Timed ability of type %@ ADDED to card %@", NSStringFromClass(self.class), card);
        self.observerAdded = YES;
        
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

- (void)dealloc {
    if (self.observerAdded) {
        [self.card.gamemanager.currentGame removeObserver:self forKeyPath:@"turnCounter"];
        self.observerAdded = NO;
    }
}

- (void)observeValueForKeyPath:(NSString *)keyPath ofObject:(id)object change:(NSDictionary *)change context:(void *)context {
    if (object == self.card.gamemanager.currentGame && [keyPath isEqualToString:@"turnCounter"]) {
        
        if (self.card.gamemanager.currentGame.turnCounter == _abilityStartedInTurn + _numberOfTurns) {
            [self notifyAndStopTimedAbility];
        }
    }
}

- (void)notifyAndStopTimedAbility {
    if (self.observerAdded) {
        [self.card.gamemanager.currentGame removeObserver:self forKeyPath:@"turnCounter"];
        NSLog(@"Timed ability of type %@ REMOVED from card %@", NSStringFromClass(self.class), self.card);

        self.observerAdded = NO;
    }
    
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
    
    if (self.card.gamemanager.currentGame.turnCounter == _abilityStartedInTurn + _numberOfTurns) {
        [self notifyAndStopTimedAbility];
    }
}

- (void)reactivateTimedAbility {
    
}

- (void)startTimedAbility {
    
    _abilityStartedInTurn = self.card.gamemanager.currentGame.turnCounter;
}

- (void)stopTimedAbility {
    
}

- (void)applyEffect {
    
}

- (BOOL)allowPerformAction:(Action*)action {
    
    return YES;
}

- (NSDictionary *)asDictionary {
    
    return [NSDictionary dictionary];
}

- (void)fromDictionary:(NSDictionary*)dictionary {
    
}

@end
