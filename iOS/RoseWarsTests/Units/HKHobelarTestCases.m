//
//  HKHobelarTestCases.m
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
#import "Archer.h"
#import "Hobelar.h"
#import "GridLocation.h"
#import "TestHelper.h"
#import "MeleeAttackAction.h"
#import "PathFinderStep.h"
#import "MoveAction.h"
#import "CardPool.h"

@interface HKHobelarTestCases : XCTestCase

@property (nonatomic) GameManager *gamemanager;

@property (nonatomic) StandardBattleStrategy *battleStrategy;

@property (nonatomic) FixedDiceStrategy *attackerFixedStrategy;
@property (nonatomic) FixedDiceStrategy *defenderFixedStrategy;


@end

@implementation HKHobelarTestCases

- (void)setUp {
    [super setUp];

    self.gamemanager = [[GameManager alloc] init];
}

- (void)tearDown {
    // Put teardown code here. This method is called after the invocation of each test method in the class.
    [super tearDown];
}

- (void)testHobelarCanMoveAfterAttackIfMovesRemaining {
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Archer *archer = (Archer*)[CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Hobelar *hobelar = (Hobelar*)[CardPool createCardOfName:kHobelar withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    hobelar.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:@[hobelar]
                                    player2Units:@[archer]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    MeleeAttackAction *meleeAttack = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:archer.cardLocation]] andCardInAction:hobelar enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    meleeAttack.delegate = mock;
    
    [meleeAttack performActionWithCompletion:^{
        XCTAssertTrue(hobelar.movesRemaining > 0, @"Chariot should have remaining moves after combat");
        XCTAssertTrue([hobelar canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Chariot should be able to move after attack");
        XCTAssertFalse([hobelar canPerformActionOfType:kActionTypeMelee withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Chariot shouldn't be able to attack a second time");
    }];
}

- (void)testHobelarCannotMoveAfterExtraActionIsConsumed {
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Archer *archer = (Archer*)[CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Hobelar *hobelar = (Hobelar*)[CardPool createCardOfName:kHobelar withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    hobelar.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:@[hobelar]
                                    player2Units:@[archer]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    MeleeAttackAction *meleeAttack = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:archer.cardLocation]] andCardInAction:hobelar enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    meleeAttack.delegate = mock;
    
    [meleeAttack performActionWithCompletion:^{
        BattlePlan *battleplan = [[BattlePlan alloc] initWithGame:self.gamemanager];
        [battleplan createBattlePlanForCard:hobelar friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards unitLayout:self.gamemanager.currentGame.unitLayout];
        XCTAssertTrue(battleplan.moveActions.count > 0, @"Hobelar should be able to move after an attack action when it stille have moves left");
        XCTAssertFalse(battleplan.meleeActions.count > 0, @"Hobelar shouldn't be able to attack twice");
        XCTAssertFalse(hobelar.extraActionConsumed, @"Extra action shouldn't be consumed");
        
        MoveAction *moveAction = battleplan.moveActions.firstObject;
        moveAction.delegate = mock;
        [moveAction performActionWithCompletion:^{
            BattlePlan *battleplan = [[BattlePlan alloc] initWithGame:self.gamemanager];
            [battleplan createBattlePlanForCard:hobelar friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards unitLayout:self.gamemanager.currentGame.unitLayout];
            XCTAssertTrue(battleplan.moveActions.count == 0, @"Hobelar shouldn't be able to move after extra action has been consumed");
            XCTAssertTrue(hobelar.extraActionConsumed, @"Extra action should be consumed");
        }];
    }];
}

@end
