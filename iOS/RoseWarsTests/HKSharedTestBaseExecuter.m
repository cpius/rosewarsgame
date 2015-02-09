//
//  HKSharedTestBaseExecuter.m
//  RoseWars
//
//  Created by Heine Kristensen on 05/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKSharedTestBaseExecuter.h"
#import "FixedDeckStrategy.h"
#import "Card.h"

@implementation HKSharedTestBaseExecuter

- (id)init
{
    self = [super init];
    if (self) {
        _gamemanager = [[GameManager alloc] init];
        _gamemanager.currentGame.myColor = kPlayerGreen;
        _gamemanager.currentGame.currentRound = 1;
        _gamemanager.currentGame.numberOfAvailableActions = 2;

        [_gamemanager.currentGame.unitLayout removeAllObjects];
}
    return self;
}

- (BOOL)executeSharedTestWithData:(NSDictionary *)data {

    NSLog(@"Executing shared test: '%@'", data[@"description"]);
    
    NSDictionary *gamestate = data[@"gamestate"];
    if (gamestate[@"actions_remaining"] != nil) {
        _gamemanager.currentGame.numberOfAvailableActions = [gamestate[@"actions_remaining"] integerValue];
    }
    
    NSDictionary *player1Units = gamestate[@"player1_units"];
    NSDictionary *player2Units = gamestate[@"player2_units"];
    
   [self setupBoardWithPlayer1Units:player1Units player2Units:player2Units];
    
    return YES;
}

- (void)setupDeckWithCards:(NSArray*)cards forPlayerWithColor:(PlayerColors)playercolor {
    
    FixedDeckStrategy *fixedDeckStrategy = [FixedDeckStrategy strategy];
    
    [fixedDeckStrategy.fixedCards removeAllObjects];
    
    for (Card *card in cards) {
        [_gamemanager.currentGame.unitLayout setObject:card forKey:card.cardLocation];
        [fixedDeckStrategy.fixedCards addObject:card];
    }

    // Player 1 is always green in testcases
    if (playercolor == kPlayerGreen) {
        _gamemanager.currentGame.myDeck = [fixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0 gamemanager:self.gamemanager];
    }
    else {
        _gamemanager.currentGame.enemyDeck = [fixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0 gamemanager:self.gamemanager];
    }
}

- (NSArray*)parseCards:(NSDictionary*)cards forPlayerWithColor:(PlayerColors)playercolor {
    
    NSArray *ignoredCards = @[@"Saboteur"];
    
    NSMutableArray *cardsForPlayer = [NSMutableArray array];
    
    for (NSString *cardLocation in cards.allKeys) {

        NSString *unittype;
        BOOL unitHasBeenUsed = NO;
        NSInteger experience = 0;
        NSInteger movementRemaining = 0;
        BOOL extraAction = NO;
        if ([cards[cardLocation] isKindOfClass:[NSDictionary class]]) {
            NSDictionary *dic = cards[cardLocation];
            
            unittype = dic[@"name"];
            unitHasBeenUsed = [dic[@"used"] boolValue];
            experience = [dic[@"experience"] integerValue];
            movementRemaining = [dic[@"movement_remaining"] integerValue];
            extraAction = [dic[@"extra_action"] boolValue];
        }
        else {
            unittype = cards[cardLocation];
        }
        
        unittype = [unittype stringByReplacingOccurrencesOfString:@" " withString:@""];
        
        if ([ignoredCards containsObject:unittype]) {
            continue;
        }
        
        Class cardClass = NSClassFromString(unittype);
        Card *card = [[cardClass alloc] init];
        
        card.gamemanager = self.gamemanager;
        card.cardLocation = [self convertLocation:cardLocation];
        card.hasPerformedActionThisRound = unitHasBeenUsed;
        if (card.isMelee) {
            card.hasPerformedAttackThisRound = unitHasBeenUsed;
        }
        card.experience = experience;
        card.movesConsumed = card.move - (card.move - movementRemaining);
        card.extraActionConsumed = !extraAction;
        
        if (playercolor == kPlayerGreen) {
            card.cardColor = kCardColorGreen;
        }
        else {
            card.cardColor = kCardColorRed;
        }
        
        if (card == nil) {
            NSLog(@"Error creating card of type: %@", unittype);
        }
        
        [cardsForPlayer addObject:card];
    }
    
    return [NSArray arrayWithArray:cardsForPlayer];
}

- (void)setupBoardWithPlayer1Units:(NSDictionary*)player1UnitData player2Units:(NSDictionary*)player2UnitData {
    
    NSArray *player1Cards = [self parseCards:player1UnitData forPlayerWithColor:kPlayerGreen];
    NSArray *player2Cards = [self parseCards:player2UnitData forPlayerWithColor:kPlayerRed];
    
    [self setupDeckWithCards:player1Cards forPlayerWithColor:kPlayerGreen];
    [self setupDeckWithCards:player2Cards forPlayerWithColor:kPlayerRed];
}

- (GridLocation*)convertLocation:(NSString*)location {
    
    if (location == nil) {
        return nil;
    }
    
    NSArray *letterColumns = @[@"", @"A", @"B", @"C", @"D", @"E"];
    
    NSInteger column = [letterColumns indexOfObject:[location substringToIndex:1]];
    NSInteger row = [location substringFromIndex:1].integerValue;
    
    return [GridLocation gridLocationWithRow:row column:column];
}

- (BOOL)evaluateOutcomeFromExpectedOutcome:(BOOL)expectedOutcome actualOutcome:(BOOL)actualOutcome {
    if (expectedOutcome) {
        return actualOutcome;
    }
    else {
        return !actualOutcome;
    }
}

@end
