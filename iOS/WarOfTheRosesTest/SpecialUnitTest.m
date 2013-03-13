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
#import "Lancer.h"
#import "RoyalGuard.h"
#import "Pikeman.h"
#import "MovePathFinderStrategy.h"
#import "Samurai.h"
#import "LightCavalry.h"
#import "Viking.h"
#import "MoveAction.h"
#import "LongSwordsMan.h"

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

- (void)testLancerGetsAttackBonusWhenAttackingWithTwoEmptyNodes {
    
    Lancer *lancer = [Lancer card];
    Archer *archer = [Archer card];
    
    lancer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    lancer.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    archer.cardColor = kCardColorRed;
        
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:lancer]
                                    player2Units:[NSArray arrayWithObjects:archer, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:lancer.cardLocation forCard:lancer enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];

    STAssertTrue(meleeAttacks.count == 1, @"Lancer should be able to attack archer");
    
    [lancer willPerformAction:meleeAttacks[0]];
    
    STAssertTrue([lancer.attack calculateValue].lowerValue == 3, @"Lancer should receive +2A bonus when 2 empty tiles before attack");
    STAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
    
    [lancer didPerformedAction:meleeAttacks[0]];
    
    [_manager endTurn];
    [_manager endTurn];

    STAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancers +2A bonus should be removed after attack");
    STAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
}

- (void)testLancerDoesntGetAttackBonusWhenAttackingWithLessThanTwoEmptyNodes {
    
    Lancer *lancer = [Lancer card];
    Archer *archer = [Archer card];
    
    lancer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    lancer.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:lancer]
                                    player2Units:[NSArray arrayWithObjects:archer, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:lancer.cardLocation forCard:lancer enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeAttacks.count == 1, @"Lancer should be able to attack archer");
    
    [lancer willPerformAction:meleeAttacks[0]];
    
    STAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancer shouldn't receive +2A bonus when only one empty tiles before attack");
    STAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
    
    [lancer didPerformedAction:meleeAttacks[0]];
    
    STAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancers +2A bonus should be removed after attack");
    STAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
}

- (void)testLancerDoesntGetAttackBonusWhenAttackingWithTwoNonEmptyNodes {
    
    Lancer *lancer = [Lancer card];
    Archer *archer = [Archer card];
    Archer *archer2 = [Archer card];
    
    lancer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    lancer.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    archer.cardColor = kCardColorRed;

    archer2.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer2.cardColor = kCardColorRed;

    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:lancer]
                                    player2Units:[NSArray arrayWithObjects:archer,archer2, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:lancer.cardLocation forCard:lancer enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeAttacks.count == 1, @"Lancer should be able to attack archer");
    
    [lancer willPerformAction:meleeAttacks[0]];
    
    STAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancer shouldn't receive +2A bonus when one of the two node are occupied");
    STAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
    
    [lancer didPerformedAction:meleeAttacks[0]];
    
    STAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancers +2A bonus should be removed after attack");
    STAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
}

- (void)testRoyalGuardGetsDefenseBonusAgainstMelee {
    
    RoyalGuard *royalguard = [RoyalGuard card];
    Pikeman *pikeman = [Pikeman card];
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    royalguard.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    pikeman.cardColor = kCardColorRed;
        
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:royalguard]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    [royalguard combatStartingAgainstAttacker:pikeman];
    
    STAssertTrue([royalguard.defence calculateValue].upperValue == 4, @"Royal guard should get +1D against melee attackers");
    
    [royalguard combatFinishedAgainstAttacker:pikeman withOutcome:kCombatOutcomeDefendSuccessful];

    STAssertTrue([royalguard.defence calculateValue].upperValue == 3, @"Royal guards defense bonus should be removed after combat");
}

- (void)testRoyalGuardGetsIncreasedMovementWhenMovingSideways {
    
    RoyalGuard *royalguard = [RoyalGuard card];
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    royalguard.cardColor = kCardColorGreen;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:royalguard]
                                    player2Units:[NSArray arrayWithObjects:nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;

    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *pathWithSidewaysMovement = [pathFinder getPathForCard:royalguard fromGridLocation:royalguard.cardLocation toGridLocation:[GridLocation gridLocationWithRow:3 column:4] usingStrategy:[MovePathFinderStrategy strategy] allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue([royalguard allowPath:pathWithSidewaysMovement forActionType:kActionTypeMove allLocations:_manager.currentGame.unitLayout], @"RoyalGuard should be able to move 2 nodes when one of them is sideways");
}

- (void)testRoyalGuardDoesntGetIncreasedMovementWhenOnlyMovingUpOrDown {
    
    RoyalGuard *royalguard = [RoyalGuard card];
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    royalguard.cardColor = kCardColorGreen;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:royalguard]
                                    player2Units:[NSArray arrayWithObjects:nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *pathWithoutSidewaysMovement = [pathFinder getPathForCard:royalguard fromGridLocation:royalguard.cardLocation toGridLocation:[GridLocation gridLocationWithRow:4 column:3] usingStrategy:[MovePathFinderStrategy strategy] allLocations:_manager.currentGame.unitLayout];
    
    STAssertFalse([royalguard allowPath:pathWithoutSidewaysMovement forActionType:kActionTypeMove allLocations:_manager.currentGame.unitLayout], @"RoyalGuard shouldn't be able to move 2 tiles when none of them is sideways");
}

- (void)testSamuraiCanAttackTwice {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Samurai *samurai = [Samurai card];
    
    LightCavalry *lightCavalry1 = [LightCavalry card];
    LightCavalry *lightCavalry2 = [LightCavalry card];
    
    samurai.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    samurai.cardColor = kCardColorGreen;
    
    lightCavalry1.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    lightCavalry1.cardColor = kCardColorRed;

    lightCavalry2.cardLocation = [GridLocation gridLocationWithRow:2 column:4];
    lightCavalry2.cardColor = kCardColorRed;

    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:samurai]
                                    player2Units:[NSArray arrayWithObjects:lightCavalry1, lightCavalry2, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];

    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:samurai.cardLocation forCard:samurai enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeAttacks.count == 2, @"Samurai should be able to attack both cavalry");
    STAssertTrue([samurai canPerformActionOfType:kActionTypeMelee withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Samurai should be able to perform melee action");
    STAssertTrue([samurai canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Samurai should be able to perform move action");
    
    MeleeAttackAction *action1 = meleeAttacks[0];
    
    action1.delegate = mock;
    
    [action1 performActionWithCompletion:^{
        STAssertTrue([samurai canPerformActionOfType:kActionTypeMelee withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Samurai should be able to perform a second melee action");
        STAssertFalse([samurai canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Samurai shouldn't be able to perform move action");
    }];
    
    MeleeAttackAction *action2 = meleeAttacks[1];
    
    action2.delegate = mock;

    [action2 performActionWithCompletion:^{
        STAssertFalse([samurai canPerformActionOfType:kActionTypeMelee withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Samurai shouldn't be able to perform a third melee action");
        STAssertFalse([samurai canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Samurai shouldn't be able to perform move action");
    }];
}

- (void)testVikingNeedsTwoSuccessfulHitsToDie {
    
    Viking *viking = [Viking card];
    Pikeman *pikeman = [Pikeman card];
    
    viking.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    viking.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:viking]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;

    STAssertTrue(viking.hitpoints == 2, @"Viking should have 2 hitpoints");

    [_manager resolveCombatBetween:pikeman defender:viking];
    
    STAssertFalse(viking.dead, @"Viking shouldn't die after a failed defense");
    STAssertTrue(viking.hitpoints == 1, @"Viking should only have 1 hitpoint left after a failed defense");
    
    [_manager resolveCombatBetween:pikeman defender:viking];
    
    STAssertTrue(viking.dead, @"Viking should be dead!");
}

- (void)testVikingCanAttackAfterMove {
    
    Viking *viking = [Viking card];
    Pikeman *pikeman = [Pikeman card];
    
    viking.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    viking.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:viking]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    MoveAction *moveAction = [[MoveAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:3 column:3]]] andCardInAction:viking enemyCard:pikeman];
    
    STAssertTrue([viking canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Viking should be able to perform move action");
    
    moveAction.delegate = mock;
    
    [moveAction performActionWithCompletion:^{
        
        STAssertFalse([viking canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Viking shouldn't be able to perform a second move action");
        
        STAssertTrue([viking canPerformActionOfType:kActionTypeMelee withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Viking should be able to perform a melee action after a move action");
        
        MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:4 column:3]]] andCardInAction:viking enemyCard:pikeman];
        
        meleeAction.delegate = mock;
        
        [meleeAction performActionWithCompletion:^{
            STAssertFalse([viking canPerformActionOfType:kActionTypeMove withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Viking shouldn't be able to perform a move action after a melee action");

            STAssertFalse([viking canPerformActionOfType:kActionTypeMelee withRemainingActionCount:_manager.currentGame.numberOfAvailableActions], @"Viking shouldn't be able to perform a second melee action");
        }];
    }];
}

- (void)testLongswordsmanHitsSurroundingEnemies {
    
    LongSwordsMan *longswordsman = [LongSwordsMan card];
    Pikeman *pikeman = [Pikeman card];
    Archer *archer = [Archer card];
    
    longswordsman.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    longswordsman.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorRed;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:longswordsman]
                                    player2Units:[NSArray arrayWithObjects:pikeman, archer, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:3 column:3]]] andCardInAction:longswordsman enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue(pikeman.dead, @"Pikeman should be dead");
        STAssertTrue(archer.dead, @"Archer should be dead");
    }];
}


@end
