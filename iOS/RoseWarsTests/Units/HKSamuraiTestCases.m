//
//  HKSamuraiTestCases.m
//  RoseWars
//
//  Created by Heine Kristensen on 06/02/15.
//  Copyright (c) 2015 Heine Skov Kristensen. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <XCTest/XCTest.h>
#import "GameManager.h"
#import "StandardBattleStrategy.h"
#import "FixedDiceStrategy.h"
#import "GameBoardMockup.h"
#import "Samurai.h"
#import "LightCavalry.h"
#import "GridLocation.h"
#import "TestHelper.h"
#import "MeleeAttackAction.h"
#import "PathFinderStep.h"
#import "MoveAction.h"
#import "PathFinder.h"
#import "Pikeman.h"
#import "CardPool.h"
#import "Catapult.h"
#import "Knight.h"

@interface HKSamuraiTestCases : XCTestCase

@property (nonatomic) GameManager *gamemanager;

@property (nonatomic) StandardBattleStrategy *battleStrategy;

@property (nonatomic) FixedDiceStrategy *attackerFixedStrategy;
@property (nonatomic) FixedDiceStrategy *defenderFixedStrategy;

@end

@implementation HKSamuraiTestCases

- (void)setUp {
    [super setUp];

    self.gamemanager = [[GameManager alloc] init];
}

- (void)tearDown {
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    [super tearDown];
}

- (void)testSamuraiCanAttackTwice {
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Samurai *samurai = [CardPool createCardOfName:kSamurai withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Catapult *catapult = [CardPool createCardOfName:kCatapult withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    samurai.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    catapult.cardLocation = [GridLocation gridLocationWithRow:2 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:samurai]
                                    player2Units:[NSArray arrayWithObjects:pikeman, catapult, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    samurai.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:2];
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    catapult.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:samurai.cardLocation forCard:samurai enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(meleeAttacks.count == 1, @"Samurai should be able to attack pikeman");
    XCTAssertTrue([samurai canPerformActionOfType:kActionTypeMelee withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Samurai should be able to perform melee action");
    XCTAssertTrue([samurai canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Samurai should be able to perform move action");
    
    MeleeAttackAction *action1 = [pathFinder getMeleeAttackActionForCard:samurai againstEnemyUnit:pikeman allLocations:self.gamemanager.currentGame.unitLayout];
    action1.meleeAttackStrategy = kMeleeAttackStrategyAutoConquer;
    
    action1.delegate = mock;
    
    [action1 performActionWithCompletion:^{
        XCTAssertTrue(pikeman.dead, @"Pikeman should be dead");
        XCTAssertTrue([samurai canPerformActionOfType:kActionTypeMelee withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Samurai should be able to perform a second melee action");
        XCTAssertFalse([samurai canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Samurai shouldn't be able to perform move action");
        XCTAssertTrue([samurai.cardLocation isSameLocationAs:pikeman.cardLocation], @"Samurai should have conquered the enemy location");
    }];
    
    MeleeAttackAction *secondaryAttack = [pathFinder getMeleeAttackActionForCard:samurai againstEnemyUnit:catapult allLocations:self.gamemanager.currentGame.unitLayout];
    XCTAssertNotNil(secondaryAttack, @"Samurai should be able to use secondary attack");
    
    secondaryAttack.delegate = mock;
    
    [secondaryAttack performActionWithCompletion:^{
        XCTAssertTrue(samurai.extraActionConsumed, @"Extra action should be consumed");
        XCTAssertFalse([samurai canPerformActionOfType:kActionTypeMelee withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Samurai shouldn't be able to perform a third melee action");
        XCTAssertFalse([samurai canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Samurai shouldn't be able to perform move action");
    }];
}

- (void)testReplayOfSamuraiSecondaryAttacks {
    Samurai *samurai = (Samurai*)[CardPool createCardOfName:kSamurai withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = (Pikeman*)[CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    samurai.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    
    self.gamemanager.currentGame.myColor = kPlayerGreen;
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                                   withPlayer1Units:[NSArray arrayWithObject:samurai]
                                                       player2Units:[NSArray arrayWithObject:defender1]];
    
    self.gamemanager.currentGame.state = kGameStateGameStarted;
    
    StandardBattleStrategy *battleStrategy = [StandardBattleStrategy strategy];
    
    battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:2];
    
    samurai.battleStrategy = battleStrategy;
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:defender1.cardLocation];
    MeleeAttackAction *firstAttack = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[step] andCardInAction:samurai enemyCard:defender1 meleeAttackType:kMeleeAttackTypeNormal];
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    firstAttack.delegate = mock;
    
    [firstAttack performActionWithCompletion:^{
        
        MeleeAttackAction *secondAttack = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[step] andCardInAction:samurai enemyCard:defender1 meleeAttackType:kMeleeAttackTypeNormal];
        secondAttack.delegate = mock;
        
        samurai.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
        defender1.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
        
        [secondAttack performActionWithCompletion:^{
            
            XCTAssertTrue(self.gamemanager.currentGame.latestBattleReports.count == 2, @"2 actions were performed");
            
            NSData *data = [self.gamemanager.currentGame serializeCurrentGameForPlayerWithId:@"TestPlayerId"];
            [self.gamemanager endTurn];
            
            [TestHelper swapBoardInGame:self.gamemanager.currentGame myCurrentGameBoardSide:kGameBoardLower];
            
            [self.gamemanager.currentGame deserializeGameData:data forPlayerWithId:@"TestPlayerId" allPlayers:@[@"TestPlayerId", @"TestPlayerId2"] onlyActions:YES onlyEnemyUnits:NO];
            
            XCTAssertTrue(self.gamemanager.currentGame.actionsForPlayback.count == 2, @"Should contain 2 actions for playback");
            
            for (Action *action in self.gamemanager.currentGame.actionsForPlayback) {
                
                action.playback = YES;
                action.delegate = mock;
                
                [action performActionWithCompletion:^{
                    
                    XCTAssertTrue(defender1.dead, @"Pikeman should be dead");
                }];
            }
        }];
    }];
}


@end
