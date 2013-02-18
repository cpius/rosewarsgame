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

@protocol GameManagerProtocol <NSObject>

- (void)turnChangedToPlayerWithColor:(PlayerColors)player;
- (void)combatHasStartedBetweenAttacker:(Card*)attacker andDefender:(Card*)defender;

@end

@interface GameManager : NSObject {
    
    AIPlayer *_enemyPlayer;
}

@property (nonatomic, weak) id<GameManagerProtocol> delegate;
@property (nonatomic, readonly) Game *currentGame;
@property (nonatomic, readonly) PlayerColors currentPlayersTurn;

- (Action*)getActionForEnemeyPlayer;
- (CombatOutcome)resolveCombatBetween:(Card*)attacker defender:(Card*)defender;

- (NSUInteger)actionUsed:(Action*)action;
- (void)startNewGameOfType:(GameTypes)gameType;
- (void)endTurn;

- (void)card:(Card*)card movedToGridLocation:(GridLocation*)location;
- (void)cardHasBeenDefeated:(Card*)card;

- (GameResults)checkForEndGame;

+ (GameManager*)sharedManager;

@end
