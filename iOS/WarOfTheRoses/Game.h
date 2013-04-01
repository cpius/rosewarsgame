//
//  Game.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/5/13.
//
//

#import <Foundation/Foundation.h>
#import "Deck.h"
#import "BattleReport.h"

@interface Game : NSObject

@property (nonatomic, assign) GameTypes gametype;

@property (nonatomic, strong) Deck *myDeck;
@property (nonatomic, strong) Deck *enemyDeck;
@property (nonatomic, assign) NSUInteger currentRound;
@property (nonatomic, assign) NSUInteger numberOfAvailableActions;
@property (nonatomic, assign) GameStates state;
@property (nonatomic, assign) PlayerColors myColor;
@property (nonatomic, assign) PlayerColors enemyColor;
@property (nonatomic, assign) BOOL gameOver;

@property (nonatomic, assign) PlayerColors currentPlayersTurn;
@property (nonatomic, strong) BattleReport *latestBattleReport;

@property (nonatomic, strong) NSMutableDictionary *unitLayout;

- (void)deserializeGameData:(NSData*)gameData;
- (NSData*)serializeCurrentGame;

- (void)populateUnitLayout;

@end
