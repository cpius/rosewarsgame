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

@interface GameManager : NSObject {
    
    AIPlayer *_enemyPlayer;
}

@property (nonatomic, readonly) Game *currentGame;

- (CombatOutcome)resolveCombatBetween:(Card*)attacker defender:(Card*)defender;

- (NSUInteger)actionUsed;
- (void)startNewGameOfType:(GameTypes)gameType;
- (void)endTurn;

- (void)card:(Card*)card movedToGridLocation:(GridLocation*)location;
- (void)cardHasBeenDefeated:(Card*)card;

+ (GameManager*)sharedManager;

@end
