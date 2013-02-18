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

- (id)initWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor {
    
    self = [super init];
    
    if (self) {
        _cards = [[RandomDeckStrategy strategy] generateNewDeckWithNumberOfBasicType:basicType andSpecialType:specialType cardColor:cardColor];
    }
    
    return self;
}



- (void)resetMoveCounters {
    
    for (Card *card in _cards) {
        card.movesConsumed = 0;
    }
}

@end
