//
//  Game.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/5/13.
//
//

#import "Game.h"
#import "CardForSerialization.h"
#import "GCTurnBasedMatchHelper.h"
#import "CardPool.h"
#import "PathFinderStep.h"

#import "MoveAction.h"

@interface Game()

- (Card*)getCardFromDeck:(Deck*)deck locatedAt:(GridLocation*)locatedAt;

@end

@implementation Game

@synthesize gametype;
@synthesize myDeck = _deck;
@synthesize enemyDeck = _enemyDeck;
@synthesize unitLayout = _unitLayout;

- (id)init {
    
    self = [super init];
    
    if (self) {
        self.myColor = arc4random() % 2;
        
        self.currentRound = 1;
        _unitLayout = [[NSMutableDictionary alloc] init];
    }
    
    return self;
}

- (PlayerColors)enemyColor {
    
    if (self.myColor == kPlayerGreen) {
        return kPlayerRed;
    }
    
    return kPlayerGreen;
}

- (void)populateUnitLayout {
    
    for (Card *card in self.myDeck.cards) {
        if (card.cardLocation != nil) {
            [self.unitLayout setObject:card forKey:card.cardLocation];
        }
    }
    
    for (Card *card in self.enemyDeck.cards) {
        if (card.cardLocation != nil) {
            [self.unitLayout setObject:card forKey:card.cardLocation];
        }
    }
}


- (NSData *)serializeCurrentGame {
    
    NSMutableDictionary *mutableGameData = [NSMutableDictionary dictionary];
    
    [mutableGameData setValue:@(_state) forKey:@"gamestate"];
    [mutableGameData setValue:@(_myColor) forKey:[GCTurnBasedMatchHelper sharedInstance].localUserId];
    [mutableGameData setValue:@(_numberOfAvailableActions) forKey:@"numberofactions"];
    [mutableGameData setValue:@(_currentRound) forKey:@"currentround"];
    [mutableGameData setValue:@(_gameOver) forKey:@"gameover"];
    [mutableGameData setValue:@(_currentPlayersTurn) forKey:@"currentplayersturn"];
    [mutableGameData setValue:@(_myColor) forKey:@"gamedata_created_by"];

    NSMutableArray *cards = [NSMutableArray array];
    
    if (_state == kGameStateFinishedPlacingCards ||
        _state == kGameStateGameStarted) {
                
        for (Card *myCard in self.myDeck.cards) {
            if (!myCard.dead) {
                CardForSerialization *serializeObject = [[CardForSerialization alloc] initWithCard:myCard];
                [cards addObject:[serializeObject asDictionary]];
            }
        }

        for (Card *enemyCard in self.enemyDeck.cards) {
            if (!enemyCard.dead) {
                CardForSerialization *serializeObject = [[CardForSerialization alloc] initWithCard:enemyCard];
                [cards addObject:[serializeObject asDictionary]];
            }
        }
        
        [mutableGameData setValue:[NSArray arrayWithArray:cards] forKey:@"cards"];
    }
    
    if (_state == kGameStateGameStarted && _latestBattleReport != nil) {
        
        NSMutableDictionary *action = [NSMutableDictionary dictionary];
        NSMutableArray *path = [NSMutableArray arrayWithCapacity:_latestBattleReport.pathTaken.count];
        
        [action setValue:@(_latestBattleReport.actionType) forKey:@"actiontype"];
        
        for (PathFinderStep *step in _latestBattleReport.pathTaken) {
            [path addObject:[NSDictionary dictionaryWithObjectsAndKeys:@(step.location.row), @"row", @(step.location.column), @"column", nil]];
        }
        
        [action setValue:[NSArray arrayWithArray:path] forKey:@"path"];
        [action setValue:@(_latestBattleReport.cardInAction.cardLocation.row) forKey:@"cardinaction_row"];
        [action setValue:@(_latestBattleReport.cardInAction.cardLocation.column) forKey:@"cardinaction_column"];
        [action setValue:@(_latestBattleReport.enemyCard.cardLocation.row) forKey:@"enemycard_row"];
        [action setValue:@(_latestBattleReport.enemyCard.cardLocation.column) forKey:@"enemycard_column"];
        
        if (_latestBattleReport.primaryBattleResult != nil) {
            [action setObject:[_latestBattleReport.primaryBattleResult asDictionary] forKey:@"primarybattle"];
        }
        
        [mutableGameData setObject:action forKey:@"action"];
    }
    
    NSDictionary *gameData = [NSDictionary dictionaryWithDictionary:mutableGameData];
    
    NSError *error = nil;
    NSData *jsonData = [NSJSONSerialization dataWithJSONObject:gameData options:kNilOptions error:&error];
    
    return jsonData;
}

- (void)deserializeGameData:(NSData*)gameData {
    
    NSError *error = nil;
    NSDictionary *data = [NSJSONSerialization JSONObjectWithData:gameData options:NSJSONReadingMutableContainers error:&error];
    
    _state = [[data objectForKey:@"gamestate"] integerValue];
    _numberOfAvailableActions = [[data objectForKey:@"numberofactions"] integerValue];
    _currentRound = [[data objectForKey:@"currentround"] integerValue];
    _gameOver = [[data objectForKey:@"gameover"] boolValue];
    _currentPlayersTurn = [[data objectForKey:@"currentplayersturn"] integerValue];
    PlayerColors creator = [[data objectForKey:@"gamedata_created_by"] integerValue];
    
    for (GKTurnBasedParticipant *participant in [GCTurnBasedMatchHelper sharedInstance].currentMatch.participants) {
        
        id color = [data valueForKey:participant.playerID];
        
        if (color != nil) {
            
            if ([participant.playerID isEqualToString:[GCTurnBasedMatchHelper sharedInstance].localUserId]) {
                _myColor = [color integerValue];
                _enemyColor = OppositeColorOf(_myColor);
            }
            else {
                _enemyColor = [color integerValue];
                _myColor = OppositeColorOf(_enemyColor);
            }
            
            break;
        }
    }
    
    NSMutableArray *myCards = [NSMutableArray array];
    NSMutableArray *enemyCards = [NSMutableArray array];
    
    if (_state == kGameStateFinishedPlacingCards ||
        _state == kGameStateGameStarted) {
        
        NSArray *cards = [data objectForKey:@"cards"];
        
        for (NSDictionary *carddata in cards) {
            
            Card *card = [CardPool createCardOfName:[[carddata objectForKey:@"unitname"] integerValue]];
            
            card.cardLocation = [GridLocation gridLocationWithRow:[[carddata objectForKey:@"row"] integerValue]
                                                           column:[[carddata objectForKey:@"column"] integerValue]];
            card.cardColor = [[carddata objectForKey:@"cardcolor"] integerValue];
            card.hitpoints = [[carddata objectForKey:@"hitpoints"] integerValue];
            card.experience = [[carddata objectForKey:@"experience"] integerValue];
            
            [card.attack addRawBonus:[[RawBonus alloc] initWithValue:[[carddata objectForKey:@"attackbonus"] integerValue]]];
            [card.defence addRawBonus:[[RawBonus alloc] initWithValue:[[carddata objectForKey:@"defensebonus"] integerValue]]];
            
            [card fromDictionary:[carddata objectForKey:@"card_specific_stats"]];
            
            if ([card isOwnedByMe]) {
                if (creator == _enemyColor) {
                    [card.cardLocation flipBacklineFromCurrentBackline:UPPER_BACKLINE];
                }
                
                [myCards addObject:card];
            }
            else {
                if (creator == _enemyColor) {
                    [card.cardLocation flipBacklineFromCurrentBackline:LOWER_BACKLINE];
                }

                [enemyCards addObject:card];
            }
        }
        
        self.myDeck = [[Deck alloc] initWithCards:myCards];
        self.enemyDeck = [[Deck alloc] initWithCards:enemyCards];
    }
    
    if (_state == kGameStateGameStarted) {
        
        NSMutableDictionary *action = [data objectForKey:@"action"];
        
        if (action != nil) {
            NSArray *path = [action objectForKey:@"path"];
            NSMutableArray *pathTaken = [NSMutableArray array];
            
            for (NSDictionary *pathStep in path) {
                
                GridLocation *location = [GridLocation gridLocationWithRow:[[pathStep valueForKey:@"row"] integerValue]
                                                                    column:[[pathStep valueForKey:@"column"] integerValue]];
                
                [pathTaken addObject:[[PathFinderStep alloc] initWithLocation:[location flipBacklineFromCurrentBackline:LOWER_BACKLINE]]];
            }
            
            ActionTypes actionType = [[action valueForKey:@"actiontype"] integerValue];
            
            GridLocation *cardInActionLocation = [GridLocation gridLocationWithRow:[[action valueForKey:@"cardinaction_row"] integerValue]
                                                                            column:[[action valueForKey:@"cardinaction_column"] integerValue]];
            
            GridLocation *enemyCardLocation = [GridLocation gridLocationWithRow:[[action valueForKey:@"enemycard_row"] integerValue]
                                                                         column:[[action valueForKey:@"enemycard_column"] integerValue]];
            
            if (actionType == kActionTypeMove) {
                
                // Get card in action from enemy deck
                Card *cardInAction = [self getCardFromDeck:self.enemyDeck locatedAt:[cardInActionLocation flipBacklineFromCurrentBackline:LOWER_BACKLINE]];
                
                // Get enemy card from my deck
                Card *enemyCard = [self getCardFromDeck:self.myDeck locatedAt:[enemyCardLocation flipBacklineFromCurrentBackline:UPPER_BACKLINE]];
                
                MoveAction *moveAction = [[MoveAction alloc] initWithPath:pathTaken andCardInAction:cardInAction
                                                                enemyCard:enemyCard];
            }
        }
    }
}

- (Card *)getCardFromDeck:(Deck *)deck locatedAt:(GridLocation *)locatedAt {
    
    for (Card *card in deck.cards) {
        
        if ([card.cardLocation isSameLocationAs:locatedAt]) {
            return card;
        }
    }
    
    return nil;
}

@end
