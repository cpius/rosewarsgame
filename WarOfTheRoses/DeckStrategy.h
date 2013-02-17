//
//  DeckStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import <Foundation/Foundation.h>
#import "Deck.h"

@protocol DeckStrategy <NSObject>

@required
- (void)placeCardsInDeck:(Deck*)deck inGameBoardSide:(GameBoardSides)gameBoardSide;

@end
