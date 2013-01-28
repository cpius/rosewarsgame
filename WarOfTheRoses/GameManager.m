//
//  GameManager.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import "GameManager.h"

@implementation GameManager

@synthesize currentGame = _currentGame;

+ (GameManager*)sharedManager {
    
    static GameManager* _instance = nil;

    @synchronized(self) {
        
        if (_instance == nil) {
            _instance = [[GameManager alloc] init];
        }
    }
    
    return _instance;
}

- (void)startNewGameOfType:(GameTypes)gameType {
    
    _currentGame = [[Game alloc] init];
    _currentGame.gametype = gameType;
    _currentGame.state = kGameStateInitialState;
    
    _currentGame.myDeck = [[Deck alloc] initWithNumberOfBasicType:7 andSpecialType:0];
    
    if (gameType == kGameTypeSinglePlayer) {
        
        _enemyPlayer = [[AIPlayer alloc] init];
        
        _currentGame.enemyDeck = [[Deck alloc] initWithNumberOfBasicType:7 andSpecialType:0];
        [_enemyPlayer placeCardsInDeck:_currentGame.enemyDeck];
    }
}

@end
