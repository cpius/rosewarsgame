//
//  AIPlayer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/22/13.
//
//

#import "AIPlayer.h"

@interface AIPlayer()

- (BOOL)deck:(Deck*)deck containsCardInLocation:(GridLocation)location;

@end

@implementation AIPlayer

- (void)placeCardsInDeck:(Deck *)deck {

    for (Card *card in deck.cards) {
        
        BOOL cardInValidPosition = NO;
        
        while (!cardInValidPosition) {
            
            GridLocation location = MakeGridLocation((arc4random() % 4) + 1, (arc4random() % 5) + 1);
            
            if (![self deck:deck containsCardInLocation:location]) {
                
                card.cardLocation = location;
                cardInValidPosition = YES;
            }
        }
    }
}

- (BOOL)deck:(Deck *)deck containsCardInLocation:(GridLocation)location {
    
    for (Card *card in deck.cards) {
        
        if (card.cardLocation.row == location.row &&
            card.cardLocation.column == location.column) {
            return YES;
        }
    }
    
    return NO;
}


@end
