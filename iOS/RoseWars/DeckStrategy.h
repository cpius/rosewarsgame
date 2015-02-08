//
//  DeckStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import <Foundation/Foundation.h>
#import "Definitions.h"

@class Deck;
@protocol DeckStrategy <NSObject>

@required

+ (id)strategy;

- (void)placeCardsInDeck:(Deck*)deck inGameBoardSide:(GameBoardSides)gameBoardSide;
- (Deck*)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor gamemanager:(GameManager*)gamemanager;

@end
