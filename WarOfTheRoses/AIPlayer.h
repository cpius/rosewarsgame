//
//  AIPlayer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/22/13.
//
//

#import <Foundation/Foundation.h>
#import "Deck.h"


@interface AIPlayer : NSObject

- (void)placeCardsInDeck:(Deck*)deck;

@end
