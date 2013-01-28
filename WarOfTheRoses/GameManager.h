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

- (void)startNewGameOfType:(GameTypes)gameType;

+ (GameManager*)sharedManager;

@end
