//
//  Deck.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 11/21/12.
//
//

#import "Deck.h"
#import "CardPool.h"

@interface Deck()

- (BOOL)cardIsAllowedInDeck:(Card*)card;

@end

@implementation Deck

@synthesize cards = _cards;

- (id)initWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType {
    
    self = [super init];
    
    if (self) {
        [self generateNewDeckWithNumberOfBasicType:basicType andSpecialType:specialType];
    }
    
    return self;
}

- (void)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType {
    
    _cards = [[NSMutableArray alloc] init];
    
    CardPool *cardPool = [[CardPool alloc] init];
        
    NSInteger numberOfBasicTypes = 0;
    NSInteger numberOfSpecialTypes = 0;
        
    while (numberOfBasicTypes < basicType) {
        
        Card *drawnCard = [cardPool drawCardOfCardType:kCardTypeBasicUnit];
        
        if ([self cardIsAllowedInDeck:drawnCard]) {
            [_cards addObject:drawnCard];
            numberOfBasicTypes++;
        }
    }
    
    while (numberOfSpecialTypes < specialType) {
        
        Card *drawnCard = [cardPool drawCardOfCardType:kCardTypeSpecialUnit];
        
        if ([self cardIsAllowedInDeck:drawnCard]) {
            [_cards addObject:drawnCard];
            numberOfSpecialTypes++;
        }
    }
}

- (BOOL)cardIsAllowedInDeck:(Card *)card {
    
    UnitName name = card.unitName;
    
    NSInteger unitsAlreadyInDeck = 0;
    
    for (Card *card in _cards) {
        if (card.unitName == name) {
            unitsAlreadyInDeck++;
        }
    }

    if (card.cardType == kCardTypeBasicUnit) {
        // Max 3 of the same basicunit allowed in the deck
        return unitsAlreadyInDeck < 3;
    }
    
    // Max 1 of the same specialunit in the deck
    return unitsAlreadyInDeck < 1;
}

@end
