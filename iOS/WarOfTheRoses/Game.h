//
//  Game.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/5/13.
//
//

#import <Foundation/Foundation.h>
#import "Deck.h"

@interface Game : NSObject

@property (nonatomic, assign) GameTypes gametype;

@property (nonatomic, strong) Deck *myDeck;
@property (nonatomic, strong) Deck *enemyDeck;
@property (nonatomic, assign) NSUInteger currentRound;
@property (nonatomic, assign) NSUInteger numberOfAvailableActions;
@property (nonatomic, assign) GameStates state;
@property (nonatomic, assign) PlayerColors myColor;
@property (nonatomic, readonly) PlayerColors enemyColor;
@property (nonatomic, assign) BOOL gameOver;

@property (nonatomic, readonly) NSMutableDictionary *unitLayout;

+ (void)deserializeGameData:(NSData*)gameData;
- (NSData*)serializeCurrentGame;

@end
