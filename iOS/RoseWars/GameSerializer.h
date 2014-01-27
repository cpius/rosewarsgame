//
//  GameSerializer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/8/13.
//
//

#import <Foundation/Foundation.h>
#import "Game.h"

@interface GameSerializer : NSObject {
    
    NSArray *_cardsBeforeAction;
    NSArray *_cardsAfterAction;
}

- (void)takeCardSnapshot:(Game *)game state:(CardSnapshotStates)state;
- (NSData*)serializeGame:(Game*)game forPlayerWithId:(NSString*)playerId;
- (void)deserializeGameData:(NSData *)gameData forPlayerWithId:(NSString*)playerId allPlayers:(NSArray*)allPlayers toGame:(Game *)game onlyActions:(BOOL)onlyActions onlyEnemyUnits:(BOOL)onlyEnemyUnits;

@end
