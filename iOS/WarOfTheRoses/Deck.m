//
//  Deck.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Deck.h"
#import "CardPool.h"
#import "RandomDeckStrategy.h"
#import "FixedDeckStrategy.h"

@interface Deck()

@end

@implementation Deck

@synthesize cards = _cards;

- (id)initWithCards:(NSArray*)cards {
    
    self = [super init];
    
    if (self) {
        _cards = cards;
    }
    
    return self;
}

- (void)resetMoveCounters {
    
    for (Card *card in _cards) {
        card.movesConsumed = 0;
        card.hasReceivedExperiencePointsThisRound = NO;
        card.hasPerformedActionThisRound = NO;
        card.hasPerformedAttackThisRound = NO;
    }
}

@end
