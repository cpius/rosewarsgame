//
//  GameSerializer.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 4/8/13.
//
//

#import <Foundation/Foundation.h>
#import "Game.h"

@interface GameSerializer : NSObject

- (NSData*)serializeGame:(Game*)game;
- (void)deserializeGameData:(NSData *)gameData toGame:(Game *)game;

@end
