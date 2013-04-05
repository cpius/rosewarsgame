//
//  GameManager.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/23/13.
//
//

#import <Foundation/Foundation.h>
#import "Game.h"
#import "AIPlayer.h"
#import "DeckStrategy.h"
#import "BattleStrategy.h"
#import "BattleResult.h"

@protocol GameManagerProtocol <NSObject>

- (void)turnChangedToPlayerWithColor:(PlayerColors)player;

- (void)combatHasStartedBetweenAttacker:(Card*)attacker andDefender:(Card*)defender;
- (void)cardHasBeenDefeatedInCombat:(Card*)card;

@end

@interface GameManager : NSObject {
    
    AIPlayer *_enemyPlayer;
    NSUInteger _turnCounter;
}

@property (nonatomic, weak) id<GameManagerProtocol> delegate;
@property (nonatomic, strong) Game *currentGame;
@property (nonatomic, assign) PlayerColors currentPlayersTurn;

@property (nonatomic, strong) id<DeckStrategy> deckStrategy;

- (Action*)getActionForEnemeyPlayer;
- (BattleResult*)resolveCombatBetween:(Card*)attacker defender:(Card*)defender battleStrategy:(id<BattleStrategy>)battleStrategy;

- (NSUInteger)actionUsed:(Action*)action;

- (void)startNewGameOfType:(GameTypes)gameType;
- (void)continueExistingGame;

- (BOOL)shouldEndTurn;
- (void)endTurn;
- (void)endGameWithGameResult:(GameResults)gameResult;

- (void)card:(Card*)card movedToGridLocation:(GridLocation*)location;
- (void)attackSuccessfulAgainstCard:(Card*)card;

- (Card*)cardLocatedAtGridLocation:(GridLocation*)gridLocation;

- (GameResults)checkForEndGame;

+ (GameManager*)sharedManager;

@end
