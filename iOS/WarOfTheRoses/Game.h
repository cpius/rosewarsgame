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

@class Action;
@class Card;
@interface Game : NSObject

@property (nonatomic, assign) GameTypes gametype;

@property (nonatomic, strong) Deck *myDeck;
@property (nonatomic, strong) Deck *enemyDeck;
@property (nonatomic, assign) NSUInteger currentRound;
@property (nonatomic, assign) NSUInteger turnCounter;
@property (nonatomic, assign) NSUInteger numberOfAvailableActions;
@property (nonatomic, assign) GameStates state;
@property (nonatomic, assign) PlayerColors myColor;
@property (nonatomic, assign) PlayerColors enemyColor;
@property (nonatomic, assign) BOOL gameOver;

@property (nonatomic, copy) NSString *localUserId;
@property (nonatomic, copy) NSString *matchId;

@property (nonatomic, assign) PlayerColors currentPlayersTurn;
@property (nonatomic, strong) BattleReport *latestBattleReport;

@property (nonatomic, strong) Action *actionForPlayback;

@property (nonatomic, strong) NSMutableDictionary *unitLayout;

- (void)deserializeGameData:(NSData*)gameData;
- (NSData*)serializeCurrentGame;

- (void)populateUnitLayout;
- (Card*)getCardFromDeck:(Deck*)deck locatedAt:(GridLocation*)locatedAt;

@end
