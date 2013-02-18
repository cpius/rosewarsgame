//
//  DeckStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/13/13.
//
//

#import <Foundation/Foundation.h>

@class Deck;
@protocol DeckStrategy <NSObject>

@required
- (void)placeCardsInDeck:(Deck*)deck inGameBoardSide:(GameBoardSides)gameBoardSide;
- (NSArray*)generateNewDeckWithNumberOfBasicType:(NSUInteger)basicType andSpecialType:(NSInteger)specialType cardColor:(CardColors)cardColor;

@end
