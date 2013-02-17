//
//  AIPlayer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/22/13.
//
//

#import "AIPlayer.h"
#import "RandomDeckStrategy.h"

@interface AIPlayer()


@end

@implementation AIPlayer


- (void)placeCardsInDeck:(Deck *)deck {
    
    RandomDeckStrategy *deckStrategy = [[RandomDeckStrategy alloc] init];
    [deckStrategy placeCardsInDeck:deck inGameBoardSide:kGameBoardUpper];
}

@end
