//
//  SpecialUnitTest.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import "SpecialUnitTest.h"
#import "Definitions.h"
#import "Hobelar.h"
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
#import "Longswordsman.h"
#import "Crusader.h"
#import "FlagBearer.h"
#import "StandardBattleStrategy.h"
#import "WarElephant.h"
#import "WarElephantBattleStrategy.h"
#import "Diplomat.h"
#import "AbilityAction.h"
#import "Juggernaut.h"
#import "JuggernautBattleStrategy.h"
#import "FixedLevelIncreaseStrategy.h"
#import "Knight.h"
#import "CardPool.h"

@interface SpecialUnitTest()

@property (nonatomic) GameManager *gamemanager;

@end

@implementation SpecialUnitTest

- (void)setUp
{
    [super setUp];
    
    self.gamemanager = [[GameManager alloc] init];
}


- (void)testBerserkerAttackingCannon {
    
    Berserker *berserker = [CardPool createCardOfName:kBerserker withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Canon *canon = [CardPool createCardOfName:kCannon withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    berserker.cardLocation = [GridLocation gridLocationWithRow:3 column:2];
    canon.cardLocation = [GridLocation gridLocationWithRow:1 column:2];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:berserker]
                                    player2Units:[NSArray arrayWithObjects:canon, nil]];
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:berserker.cardLocation forCard:berserker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(meleeAttacks.count == 1, @"Berserker should be able to attack cannon");
}


- (void)testScoutCannotMoveFirstRound {
    
    Scout *scout = [CardPool createCardOfName:kScout withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    scout.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:scout]
                                    player2Units:[NSArray arrayWithObjects:nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;

    BOOL canPerformAction = [scout canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions];
    
    XCTAssertFalse(canPerformAction, @"Scout should not be able to move in the first round");
    
    [self.gamemanager endTurn];
    [self.gamemanager endTurn];
    
    canPerformAction = [scout canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions];

    XCTAssertTrue(canPerformAction, @"Scout should be able to move when past the first round");
}

- (void)testBerserkerCanAttackEnemyUnitWithFourNodes {
    
    Berserker *berserker = [CardPool createCardOfName:kBerserker withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Hobelar *chariot = [CardPool createCardOfName:kHobelar withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    berserker.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    chariot.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:berserker]
                                    player2Units:[NSArray arrayWithObjects:chariot, archer, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:berserker.cardLocation forCard:berserker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];

    XCTAssertTrue(meleeAttacks.count == 1, @"Berserker should be able to attack chariot");
    
    NSArray *moveActions = [pathFinder getMoveActionsFromLocation:berserker.cardLocation forCard:berserker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(moveActions.count == 4, @"Berserker should only be able to move to adjacent nodes");
}

- (void)testLancerGetsAttackBonusWhenAttackingWithTwoEmptyNodes {
    
    Lancer *lancer = [CardPool createCardOfName:kLancer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    lancer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:lancer]
                                    player2Units:[NSArray arrayWithObjects:archer, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:lancer.cardLocation forCard:lancer enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];

    XCTAssertTrue(meleeAttacks.count == 1, @"Lancer should be able to attack archer");
    
    [lancer willPerformAction:meleeAttacks[0]];
    
    XCTAssertTrue([lancer.attack calculateValue].lowerValue == 3, @"Lancer should receive +2A bonus when 2 empty tiles before attack");
    XCTAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
    
    [lancer didPerformedAction:meleeAttacks[0]];
    
    [self.gamemanager endTurn];
    [self.gamemanager endTurn];

    XCTAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancers +2A bonus should be removed after attack");
    XCTAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
}

- (void)testLancerDoesntGetAttackBonusWhenAttackingWithLessThanTwoEmptyNodes {
    
    Lancer *lancer = [CardPool createCardOfName:kLancer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    lancer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:lancer]
                                    player2Units:[NSArray arrayWithObjects:archer, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:lancer.cardLocation forCard:lancer enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(meleeAttacks.count == 1, @"Lancer should be able to attack archer");
    
    [lancer willPerformAction:meleeAttacks[0]];
    
    XCTAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancer shouldn't receive +2A bonus when only one empty tiles before attack");
    XCTAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
    
    [lancer didPerformedAction:meleeAttacks[0]];
    
    XCTAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancers +2A bonus should be removed after attack");
    XCTAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
}

- (void)testLancerDoesntGetAttackBonusWhenAttackingWithTwoNonEmptyNodes {
    
    Lancer *lancer = [CardPool createCardOfName:kLancer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *archer2 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    lancer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    archer2.cardLocation = [GridLocation gridLocationWithRow:4 column:3];

    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:lancer]
                                    player2Units:[NSArray arrayWithObjects:archer,archer2, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAttacks = [pathFinder getMeleeAttackActionsFromLocation:lancer.cardLocation forCard:lancer enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(meleeAttacks.count == 1, @"Lancer should be able to attack archer");
    
    [lancer willPerformAction:meleeAttacks[0]];
    
    XCTAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancer shouldn't receive +2A bonus when one of the two node are occupied");
    XCTAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
    
    [lancer didPerformedAction:meleeAttacks[0]];
    
    XCTAssertTrue([lancer.attack calculateValue].lowerValue == 5, @"Lancers +2A bonus should be removed after attack");
    XCTAssertTrue([lancer.attack calculateValue].upperValue == 6, @"Lancer upper attack value should remain unchanfed");
}

- (void)testRoyalGuardGetsDefenseBonusAgainstMelee {
    
    RoyalGuard *royalguard = [CardPool createCardOfName:kRoyalGuard withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:royalguard]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    [royalguard combatStartingAgainstAttacker:pikeman];
    
    XCTAssertTrue([royalguard.defence calculateValue].upperValue == 4, @"Royal guard should get +1D against melee attackers");
    
    [royalguard combatFinishedAgainstAttacker:pikeman withOutcome:kCombatOutcomeDefendSuccessful];

    XCTAssertTrue([royalguard.defence calculateValue].upperValue == 3, @"Royal guards defense bonus should be removed after combat");
}

- (void)testRoyalGuardGetsIncreasedMovementWhenMovingSideways {
    
    RoyalGuard *royalguard = [CardPool createCardOfName:kRoyalGuard withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:royalguard]
                                    player2Units:[NSArray arrayWithObjects:nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;

    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *pathWithSidewaysMovement = [pathFinder getPathForCard:royalguard fromGridLocation:royalguard.cardLocation toGridLocation:[GridLocation gridLocationWithRow:3 column:4] usingStrategy:[MovePathFinderStrategy strategy] allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue([royalguard allowPath:pathWithSidewaysMovement forActionType:kActionTypeMove allLocations:self.gamemanager.currentGame.unitLayout], @"RoyalGuard should be able to move 2 nodes when one of them is sideways");
}

- (void)testRoyalGuardDoesntGetIncreasedMovementWhenOnlyMovingUpOrDown {
    
    RoyalGuard *royalguard = [CardPool createCardOfName:kRoyalGuard withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:royalguard]
                                    player2Units:[NSArray arrayWithObjects:nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *pathWithoutSidewaysMovement = [pathFinder getPathForCard:royalguard fromGridLocation:royalguard.cardLocation toGridLocation:[GridLocation gridLocationWithRow:4 column:3] usingStrategy:[MovePathFinderStrategy strategy] allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertFalse([royalguard allowPath:pathWithoutSidewaysMovement forActionType:kActionTypeMove allLocations:self.gamemanager.currentGame.unitLayout], @"RoyalGuard shouldn't be able to move 2 tiles when none of them is sideways");
}


- (void)testVikingNeedsTwoSuccessfulHitsToDie {
    
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    viking.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:viking]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    viking.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    pikeman.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];

    XCTAssertTrue(viking.hitpoints == 2, @"Viking should have 2 hitpoints");

    [self.gamemanager resolveCombatBetween:pikeman defender:viking battleStrategy:pikeman.battleStrategy];
    
    XCTAssertFalse(viking.dead, @"Viking shouldn't die after a failed defense");
    XCTAssertTrue(viking.hitpoints == 1, @"Viking should only have 1 hitpoint left after a failed defense");
    
    [self.gamemanager resolveCombatBetween:pikeman defender:viking battleStrategy:pikeman.battleStrategy];
    
    XCTAssertTrue(viking.dead, @"Viking should be dead!");
}

- (void)testVikingCanAttackAfterMove {
    
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    viking.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:viking]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    MoveAction *moveAction = [[MoveAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:3 column:3]]] andCardInAction:viking enemyCard:pikeman];
    
    XCTAssertTrue([viking canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Viking should be able to perform move action");
    
    moveAction.delegate = mock;
    
    [moveAction performActionWithCompletion:^{
        
        XCTAssertFalse([viking canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Viking shouldn't be able to perform a second move action");
        
        XCTAssertTrue([viking canPerformActionOfType:kActionTypeMelee withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Viking should be able to perform a melee action after a move action");
        
        MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:4 column:3]]] andCardInAction:viking enemyCard:pikeman];
        
        meleeAction.delegate = mock;
        
        [meleeAction performActionWithCompletion:^{
            XCTAssertFalse([viking canPerformActionOfType:kActionTypeMove withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Viking shouldn't be able to perform a move action after a melee action");

            XCTAssertFalse([viking canPerformActionOfType:kActionTypeMelee withRemainingActionCount:self.gamemanager.currentGame.numberOfAvailableActions], @"Viking shouldn't be able to perform a second melee action");
        }];
    }];
}

- (void)testLongswordsmanHitsSurroundingEnemies {
    
    Longswordsman *longswordsman = [CardPool createCardOfName:kLongswordsman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    longswordsman.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:longswordsman]
                                    player2Units:[NSArray arrayWithObjects:pikeman, archer, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    longswordsman.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    archer.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];

    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:3 column:3]]] andCardInAction:longswordsman enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertTrue(pikeman.dead, @"Pikeman should be dead");
        XCTAssertTrue(archer.dead, @"Archer should be dead");
    }];
}


- (void)testCardAdjacentToCrusaderIsAffectedByAoeEffect {
    
    Crusader *crusader = [CardPool createCardOfName:kCrusader withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    crusader.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:crusader, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:3 column:3]]] andCardInAction:pikeman enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{

        XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 4, @"Pikeman should have received +1A aoe effect from Crusader");
    }];
}

- (void)testCardNotAdjacentToCrusaderIsNotAffectedByAoeEffect {
    
    Crusader *crusader = [CardPool createCardOfName:kCrusader withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    crusader.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:7 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:7 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:crusader, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:7 column:4]]] andCardInAction:pikeman enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikeman should have received +1A aoe effect from Crusader");
    }];
}

- (void)testCardRecievesAttackBonusWhileAdjacentToFlagBearer {
    
    FlagBearer *flagbearer = [CardPool createCardOfName:kFlagBearer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:flagbearer, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:archer.cardLocation]] andCardInAction:pikeman enemyCard:archer];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 3, @"Pikeman should have received +1A aoe effect from Crusader");
    }];
}

- (void)testWarElephantPushesEnemyWhenDefenseIsSuccesful {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:pikeman]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:warelephant enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    warelephant.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:1];
        
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertTrue(pikeman.cardLocation.row == 4, @"Pikeman should be pushed");
        XCTAssertTrue(pikeman.cardLocation.column == 3, @"Pikeman should be pushed");
    }];
}

- (void)testWarElephantKillsEnemyWhenPushedOutOfGameBoard {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:1 column:4];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:1 column:5];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:pikeman]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:warelephant enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    warelephant.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:1];
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertTrue(pikeman.dead, @"Pikeman should be dead");
    }];
}


- (void)testWarElephantPushesVikingAndVikingLosesOneHitPoint {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:viking]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:warelephant enemyCard:viking];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    warelephant.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    viking.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertFalse(viking.dead, @"Viking should survice attack");
        XCTAssertTrue(viking.hitpoints == 1, @"Viking should only have 1 hitpoint left");
        XCTAssertTrue(viking.cardLocation.row == 4, @"Viking should be pushed");
        XCTAssertTrue(viking.cardLocation.column == 3, @"Viking should be pushed");
    }];
}

- (void)testWarElephantKillsVikingIfPushIsNotPossible {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObjects:viking, pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:warelephant enemyCard:viking];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    warelephant.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    viking.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertTrue(viking.dead, @"Viking should be dead");
        XCTAssertTrue(viking.hitpoints == 0, @"Viking should be dead");
        XCTAssertFalse(pikeman.dead, @"Pikeman should survice");
    }];
}


- (void)testWarElephantHitsSurroundingEnemies {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *defender1 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *defender2 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *defender3 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    
    defender1.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender2.cardLocation = [GridLocation gridLocationWithRow:3 column:2];
    defender3.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:defender1.cardLocation]] andCardInAction:warelephant enemyCard:defender1];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    defender1.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:2];
    defender2.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender3.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    warelephant.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];

    StandardBattleStrategy *aoeBattleStrategy = [StandardBattleStrategy strategy];
    aoeBattleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    warelephant.aoeBattleStrategy = aoeBattleStrategy;
    
    [meleeAction performActionWithCompletion:^{
        XCTAssertTrue(defender1.cardLocation.row == 4, @"Pikeman should be pushed");
        XCTAssertTrue(defender1.cardLocation.column == 3, @"Pikeman should be pushed");
        
        XCTAssertTrue(defender2.dead, @"Pikeman2 should be dead");
        XCTAssertTrue(defender3.dead, @"Pikeman3 should be dead");
    }];
}

- (void)testWarElephantPushesVikingWithoutLossOfLifeIfVikingDefenseIsSuccessful {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:viking]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:warelephant enemyCard:viking];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    warelephant.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    viking.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:2];
    
    [meleeAction performActionWithCompletion:^{
        
        XCTAssertFalse(viking.dead, @"Viking should be alive");
        XCTAssertTrue(viking.hitpoints == 2, @"Viking should still have 2 hitpoints");
        XCTAssertTrue(viking.cardLocation.row == 4, @"Viking should be pushed");
        XCTAssertTrue(viking.cardLocation.column == 3, @"Viking should be pushed");
    }];
}

- (void)testVikingShouldBeAbleToPerformMeleeActionWithoutConquerAgainstUnitsInRangeTwo {
    
    WarElephant *warelephant = [CardPool createCardOfName:kWarElephant withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    warelephant.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:viking]
                                    player2Units:[NSArray arrayWithObject:warelephant]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    
    NSArray *meleeAactions = [pathFinder getMeleeAttackActionsFromLocation:viking.cardLocation forCard:viking enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(meleeAactions.count == 1, @"Viking should be able to attack warelephant in range 2");

    MeleeAttackAction *action = meleeAactions[0];
    XCTAssertTrue(action.meleeAttackType == kMeleeAttackTypeNormal, @"Viking shouldn't be able to conquer warelephant");
}

- (void)testLongswordsmanCannotMoveAfterAttack {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];

    Samurai *samurai = [CardPool createCardOfName:kSamurai withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    samurai.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:samurai]
                                    player2Units:[NSArray arrayWithObjects:pikeman, archer, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    archer.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];

    PathFinder *pathfinder = [[PathFinder alloc ]initWithGameManager:self.gamemanager];
    MeleeAttackAction *action = [pathfinder getMeleeAttackActionForCard:samurai againstEnemyUnit:pikeman allLocations:self.gamemanager.currentGame.unitLayout];
    action.delegate = mock;

    samurai.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];

    XCTAssertTrue(action.meleeAttackType == kMeleeAttackTypeConquer, @"Samurai should be able to attack&conquer pikeman");
    action.meleeAttackStrategy = kMeleeAttackStrategyAutoConquer;
    
    [action performActionWithCompletion:^{
        
        MeleeAttackAction *secondaryAttack = [pathfinder getMeleeAttackActionForCard:samurai againstEnemyUnit:archer allLocations:self.gamemanager.currentGame.unitLayout];
        
        XCTAssertNotNil(secondaryAttack, @"Samurai should be able to make a secondary attack");
        XCTAssertTrue(secondaryAttack.meleeAttackType == kMeleeAttackTypeNormal, @"Samurai shouldn't be able to attack&conquer archer");
    }];
}

- (void)testDiplomatSpecialAbility {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];

    Diplomat *diplomat = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    diplomat.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:diplomat]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathfinder = [[PathFinder alloc ] initWithGameManager:self.gamemanager];
    NSArray *actions = [pathfinder getAbilityActionsFromLocation:diplomat.cardLocation
                                                         forCard:diplomat
                                                   friendlyUnits:self.gamemanager.currentGame.myDeck.cards
                                                      enemyUnits:self.gamemanager.currentGame.enemyDeck.cards
                                                    allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertNotNil(actions, @"Diplomat should be able to bribe pikeman");
    
    AbilityAction *action = actions[0];
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        XCTAssertTrue(pikeman.cardColor == diplomat.cardColor, @"Pikeman should now be green");
        XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 4, @"Pikeman should have +1A when bribed");
        
        [self.gamemanager endTurn];
        
        XCTAssertTrue(pikeman.cardColor == kCardColorRed, @"Pikeman should be red again");
        XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikemans attackbonus from bribe should be gone");
        XCTAssertTrue([pikeman isAffectedByAbility:kAbilityCoolDown], @"Pikeman is affected by cooldown");
        
        [self.gamemanager endTurn];
        
        XCTAssertTrue([pikeman isAffectedByAbility:kAbilityCoolDown], @"Pikeman should no longer be affected by cooldown");
        
        [self.gamemanager endTurn];

        XCTAssertFalse([pikeman isAffectedByAbility:kAbilityCoolDown], @"Pikeman should no longer be affected by cooldown");
    }];
}

- (void)testJuggernautAlwaysPushedOnSuccessfulAttack {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Juggernaut *juggernaut = [CardPool createCardOfName:kJuggernaut withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    juggernaut.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:juggernaut]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:juggernaut enemyCard:pikeman meleeAttackType:kMeleeAttackTypeConquer];
    action.meleeAttackStrategy = kMeleeAttackStrategyAutoConquer;
    
    FixedDiceStrategy *attackerFixedStrategy = [FixedDiceStrategy strategyWithFixedValue:6];

    JuggernautBattleStrategy *battleStrategy = (JuggernautBattleStrategy*)[juggernaut newBattleStrategy];
    battleStrategy.attackerDiceStrategy = attackerFixedStrategy;
    juggernaut.battleStrategy = battleStrategy;
    
    action.delegate = mock;
    
    [action performActionWithCompletion:^{

        XCTAssertFalse(pikeman.dead, @"Pikeman should be alive");
        XCTAssertTrue([pikeman.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:3]], @"Pikeman should be pushed");
        XCTAssertTrue([juggernaut.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:4]], @"Juggernaut should have conquered pikemans location");
        XCTAssertTrue([action.gridLocationForConquer isSameLocationAs:[GridLocation gridLocationWithRow:4 column:4]], @"Juggernaut should have conquered pikemans location");
    }];
}

- (void)testJuggernautAlwaysPushedOnSuccessfulAttackKeepOriginalPositionWhenNotConquer {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Juggernaut *juggernaut = [CardPool createCardOfName:kJuggernaut withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    juggernaut.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:juggernaut]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:juggernaut enemyCard:pikeman meleeAttackType:kMeleeAttackTypeNormal];
    
    FixedDiceStrategy *attackerFixedStrategy = [FixedDiceStrategy strategyWithFixedValue:6];
    
    JuggernautBattleStrategy *battleStrategy = (JuggernautBattleStrategy*)[juggernaut newBattleStrategy];
    battleStrategy.attackerDiceStrategy = attackerFixedStrategy;
    juggernaut.battleStrategy = battleStrategy;
    
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        XCTAssertFalse(pikeman.dead, @"Pikeman should be alive");
        XCTAssertTrue([pikeman.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:3]], @"Pikeman should be pushed");
        XCTAssertTrue([juggernaut.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:5]], @"Juggernaut should have conquered pikemans location");
    }];
}

- (void)testJuggernautCannotConquerEnemyWhenMoreThanOneHitPoint {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Juggernaut *juggernaut = [CardPool createCardOfName:kJuggernaut withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Viking *viking = [CardPool createCardOfName:kViking withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    juggernaut.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    viking.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:juggernaut]
                                    player2Units:[NSArray arrayWithObjects:viking, pikeman, nil]];
    
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:juggernaut enemyCard:viking meleeAttackType:kMeleeAttackTypeConquer];
    
    FixedDiceStrategy *attackerFixedStrategy = [FixedDiceStrategy strategyWithFixedValue:6];
    
    JuggernautBattleStrategy *battleStrategy = (JuggernautBattleStrategy*)[juggernaut newBattleStrategy];
    battleStrategy.attackerDiceStrategy = attackerFixedStrategy;
    juggernaut.battleStrategy = battleStrategy;
    
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        XCTAssertFalse(viking.dead, @"Viking should be alive");
        XCTAssertTrue(viking.hitpoints == 1, @"Viking should have lost a hitpoint");
        XCTAssertTrue([viking.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:4]], @"Viking wasn't pushed");
        XCTAssertTrue([juggernaut.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:5]], @"Juggernaut should have original position");
    }];
}


- (void)testEnemyShouldEndTurnWhenOnlyTwoUnitsLeftAndOnOfThemAreOnBribeCooldown {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Diplomat *diplomat = [CardPool createCardOfName:kDiplomat withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    diplomat.cardLocation = [GridLocation gridLocationWithRow:6 column:1];
    
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    archer.cardLocation = [GridLocation gridLocationWithRow:2 column:4];
    
    Knight *heavycavalry = [CardPool createCardOfName:kKnight withCardColor:kCardColorRed gamemanager:self.gamemanager];
    heavycavalry.cardLocation = [GridLocation gridLocationWithRow:6 column:3];

    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager withPlayer1Units:@[diplomat] player2Units:@[archer, heavycavalry]];
    self.gamemanager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    NSArray *actions = [pathfinder getAbilityActionsFromLocation:diplomat.cardLocation forCard:diplomat friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(actions.count == 1, @"Diplomat should be able to bribe heavycavalry");
    
    AbilityAction *bribe = actions[0];
    bribe.delegate = mock;
    [bribe performActionWithCompletion:^{
        XCTAssertTrue([heavycavalry isAffectedByAbility:kAbilityBribe], @"Heavycavalry should be bribed");
        [self.gamemanager endTurn];
        XCTAssertTrue([heavycavalry isAffectedByAbility:kAbilityCoolDown], @"Heavycavalry should be affected by cooldown");
        
        NSArray *archerActions = [pathfinder getMoveActionsFromLocation:archer.cardLocation forCard:archer enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
        XCTAssertTrue(archerActions.count > 0, @"Archer should be able to move");
        
        NSArray *heavycavalryActions = [pathfinder getMoveActionsFromLocation:heavycavalry.cardLocation forCard:heavycavalry enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
        XCTAssertTrue(heavycavalryActions.count == 0, @"Heavycavalry shouldn't be able to move because of cooldown");
        
        MoveAction *moveAction = archerActions[0];
        moveAction.delegate = mock;
        [moveAction performActionWithCompletion:^{
            XCTAssertTrue([self.gamemanager shouldEndTurn], @"Should end turn now even though one action is still available, but heavycavalry has cooldown, so enemy has no more legal moves");
        }];
    }];
}

@end
