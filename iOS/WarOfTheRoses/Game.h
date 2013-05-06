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
@class GameSerializer;
@interface Game : NSObject {
    
    GameSerializer *_gameSerializer;
}

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
@property (nonatomic, strong) NSMutableArray *latestBattleReports;

@property (nonatomic, strong) NSMutableArray *actionsForPlayback;

@property (nonatomic, strong) NSMutableDictionary *unitLayout;

- (void)addBattleReport:(BattleReport*)battlereport forAction:(Action*)action;
- (void)deserializeGameData:(NSData *)gameData forPlayerWithId:(NSString*)playerId allPlayers:(NSArray*)allPlayers onlyActions:(BOOL)onlyActions onlyEnemyUnits:(BOOL)onlyEnemyUnits;
- (NSData*)serializeCurrentGameForPlayerWithId:(NSString*)playerId;
- (void)takeCardSnapshot:(CardSnapshotStates)state;

- (void)populateUnitLayout;
- (Card*)getCardFromDeck:(Deck*)deck locatedAt:(GridLocation*)locatedAt;

@end
