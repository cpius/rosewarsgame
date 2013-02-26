//
//  BaseDeckStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import "BaseDeckStrategy.h"
#import "GridLocation.h"
#import "Card.h"
#import "Deck.h"

@implementation BaseDeckStrategy

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

- (BOOL)deck:(Deck *)deck containsCardInLocation:(GridLocation*)location {
    
    for (Card *card in deck.cards) {
        
        if ([card.cardLocation isEqual:location]) {
            return YES;
        }
    }
    
    return NO;
}

@end
