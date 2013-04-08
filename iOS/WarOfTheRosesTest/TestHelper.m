//
//  TestHelper.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import "TestHelper.h"
#import "Definitions.h"
#import "Card.h"
#import "FixedDeckStrategy.h"
#import "Game.h"

@implementation TestHelper

+ (Game *)setupGame:(Game*)game withPlayer1Units:(NSArray *)player1Units player2Units:(NSArray *)player2Units {

    FixedDeckStrategy *attackerFixedDeckStrategy = [FixedDeckStrategy strategy];
    FixedDeckStrategy *defenderFixedDeckStrategy = [FixedDeckStrategy strategy];

    [game.unitLayout removeAllObjects];
    
    [attackerFixedDeckStrategy.fixedCards removeAllObjects];
    [defenderFixedDeckStrategy.fixedCards removeAllObjects];
    
    for (Card *card in player1Units) {
        [game.unitLayout setObject:card forKey:card.cardLocation];
        
        [attackerFixedDeckStrategy.fixedCards addObject:card];
    }
    
    for (Card *card in player2Units) {
        [game.unitLayout setObject:card forKey:card.cardLocation];
        
        [defenderFixedDeckStrategy.fixedCards addObject:card];
    }
    
    game.myDeck = [attackerFixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0];
    game.enemyDeck = [defenderFixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0];
    
    game.currentRound = 1;
    game.numberOfAvailableActions = 1;
    
    // During unittests myColor is always green
    game.myColor = kPlayerGreen;
    
    return game;
}

@end
