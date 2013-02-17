//
//  RandomDeckStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import "RandomDeckStrategy.h"

@implementation RandomDeckStrategy

- (void)placeCardsInDeck:(Deck *)deck inGameBoardSide:(GameBoardSides)gameBoardSide {
    
    NSUInteger offset = 0;
    
    for (Card *card in deck.cards) {
        
        BOOL cardInValidPosition = NO;
        
        while (!cardInValidPosition) {
            
            GridLocation *location = [GridLocation gridLocationWithRow:(arc4random() % 4) + 1 + offset column:(arc4random() % 5) + 1];
            
            if (![self deck:deck containsCardInLocation:location]) {
                
                card.cardLocation = location;
                cardInValidPosition = YES;
            }
        }
    }
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
