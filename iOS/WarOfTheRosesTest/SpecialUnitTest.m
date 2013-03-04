//
//  SpecialUnitTest.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import "SpecialUnitTest.h"
#import "Definitions.h"
#import "Chariot.h"
#import "Archer.h"
#import "GameManager.h"
#import "TestHelper.h"
#import "GameBoardMockup.h"
#import "MeleeAttackAction.h"
#import "PathFinder.h"
#import "PathFinderStep.h"
#import "Berserker.h"
#import "Scout.h"
#import "Canon.h"

@implementation SpecialUnitTest

- (void)setUp
{
    [super setUp];
    
    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
    
    _manager.attackerDiceStrategy = _attackerFixedStrategy;
    _manager.defenderDiceStrategy = _defenderFixedStrategy;
}

- (void)testChariotCanMoveAfterAttack {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Archer *archer = [Archer card];
    Chariot *chariot = [Chariot card];
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    archer.cardColor = kCardColorRed;
    
    chariot.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    chariot.cardColor = kCardColorGreen;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:chariot]
                                    player2Units:[NSArray arrayWithObjects:archer, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    MeleeAttackAction *meleeAttack = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:archer.cardLocation]] andCardInAction:chariot enemyCard:archer];
    
    meleeAttack.delegate = mock;
    
    [meleeAttack performActionWithCompletion:^{
        STAssertTrue(chariot.movesRemaining > 0, @"Chariot should have remaining moves after combat");
        STAssertTrue([chariot canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Chariot should be able to move after attack");
        STAssertFalse([chariot canPerformActionOfType:kActionTypeMelee withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Chariot shouldn't be able to attack a second time");
    }];
}

- (void)testBerserkerAttackingCannon {
    
    Berserker *berserker = [Berserker card];
    Canon *canon = [Canon card];
    
    berserker.cardLocation = [GridLocation gridLocationWithRow:3 column:2];
    berserker.cardColor = kCardColorGreen;
    
    canon.cardLocation = [GridLocation gridLocationWithRow:1 column:2];
    canon.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:berserker]
                                    player2Units:[NSArray arrayWithObjects:canon, nil]];
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:berserker.cardLocation forCard:berserker enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeAttacks.count == 1, @"Berserker should be able to attack cannon");
}


- (void)testScoutCannotMoveFirstRound {
    
    Scout *scout = [Scout card];
    
    scout.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    scout.cardColor = kCardColorGreen;
        
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:scout]
                                    player2Units:[NSArray arrayWithObjects:nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;

    BOOL canPerformAction = [scout canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions];
    
    STAssertFalse(canPerformAction, @"Scout should not be able to move in the first round");
    
    [_manager endTurn];
    [_manager endTurn];
    
    canPerformAction = [scout canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions];

    STAssertTrue(canPerformAction, @"Scout should be able to move when past the first round");
}

- (void)testBerserkerCanAttackEnemyUnitWithFourNodes {
    
    Berserker *berserker = [Berserker card];
    Chariot *chariot = [Chariot card];
    Archer *archer = [Archer card];
    
    berserker.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    berserker.cardColor = kCardColorGreen;
    
    chariot.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    chariot.cardColor = kCardColorRed;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:berserker]
                                    player2Units:[NSArray arrayWithObjects:chariot, archer, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:berserker.cardLocation forCard:berserker enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];

    STAssertTrue(meleeAttacks.count == 1, @"Berserker should be able to attack chariot");
    
    NSArray *moveActions = [pathFinder getMoveActionsFromLocation:berserker.cardLocation forCard:berserker enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(moveActions.count == 4, @"Berserker should only be able to move to adjacent nodes");
}

@end
