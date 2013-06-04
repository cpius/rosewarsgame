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
#import "Crusader.h"
#import "FlagBearer.h"
#import "StandardBattleStrategy.h"
#import "WarElephant.h"
#import "WarElephantBattleStrategy.h"
#import "Diplomat.h"
#import "AbilityAction.h"
#import "Juggernaut.h"
#import "JuggernautBattleStrategy.h"

@implementation SpecialUnitTest

- (void)setUp
{
    [super setUp];
    
    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
    
    _battleStrategy = [StandardBattleStrategy strategy];
    
    _battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    _battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
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
    
    MeleeAttackAction *meleeAttack = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:archer.cardLocation]] andCardInAction:chariot enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
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

    [_manager resolveCombatBetween:pikeman defender:viking battleStrategy:_battleStrategy];
    
    STAssertFalse(viking.dead, @"Viking shouldn't die after a failed defense");
    STAssertTrue(viking.hitpoints == 1, @"Viking should only have 1 hitpoint left after a failed defense");
    
    [_manager resolveCombatBetween:pikeman defender:viking battleStrategy:_battleStrategy];
    
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
    longswordsman.battleStrategy = _battleStrategy;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue(pikeman.dead, @"Pikeman should be dead");
        STAssertTrue(archer.dead, @"Archer should be dead");
    }];
}


- (void)testCardAdjacentToCrusaderIsAffectedByAoeEffect {
    
    Crusader *crusader = [Crusader card];
    Pikeman *pikeman = [Pikeman card];
    Archer *archer = [Archer card];
    
    crusader.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    crusader.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObjects:crusader, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:3 column:3]]] andCardInAction:pikeman enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{

        STAssertTrue([pikeman.attack calculateValue].lowerValue == 4, @"Pikeman should have received +1A aoe effect from Crusader");
    }];
}

- (void)testCardNotAdjacentToCrusaderIsNotAffectedByAoeEffect {
    
    Crusader *crusader = [Crusader card];
    Pikeman *pikeman = [Pikeman card];
    Archer *archer = [Archer card];
    
    crusader.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    crusader.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:7 column:3];
    pikeman.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:7 column:4];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObjects:crusader, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:7 column:4]]] andCardInAction:pikeman enemyCard:archer meleeAttackType:kMeleeAttackTypeConquer];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikeman should have received +1A aoe effect from Crusader");
    }];
}

- (void)testCardRecievesAttackBonusWhileAdjacentToFlagBearer {
    
    FlagBearer *flagbearer = [FlagBearer card];
    Pikeman *pikeman = [Pikeman card];
    Archer *archer = [Archer card];
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    flagbearer.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObjects:flagbearer, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:archer]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:archer.cardLocation]] andCardInAction:pikeman enemyCard:archer];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue([pikeman.attack calculateValue].lowerValue == 3, @"Pikeman should have received +1A aoe effect from Crusader");
    }];
}

- (void)testWarElephantPushesEnemyWhenDefenseIsSuccesful {
    
    WarElephant *warelephant = [WarElephant card];
    Pikeman *pikeman = [Pikeman card];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    warelephant.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorRed;
    
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:pikeman]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:warelephant enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    BaseBattleStrategy *battleStrategy = warelephant.battleStrategy;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 1;

    battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
        
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue(pikeman.cardLocation.row == 4, @"Pikeman should be pushed");
        STAssertTrue(pikeman.cardLocation.column == 3, @"Pikeman should be pushed");
    }];
}

- (void)testWarElephantKillsEnemyWhenPushedOutOfGameBoard {
    
    WarElephant *warelephant = [WarElephant card];
    Pikeman *pikeman = [Pikeman card];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:1 column:4];
    warelephant.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:1 column:5];
    pikeman.cardColor = kCardColorRed;
    
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:pikeman]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:warelephant enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    BaseBattleStrategy *battleStrategy = warelephant.battleStrategy;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 1;
    
    battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue(pikeman.dead, @"Pikeman should be dead");
    }];
}


- (void)testWarElephantPushesVikingAndVikingLosesOneHitPoint {
    
    WarElephant *warelephant = [WarElephant card];
    Viking *viking = [Viking card];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    warelephant.cardColor = kCardColorGreen;
    
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    viking.cardColor = kCardColorRed;
    
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:viking]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:warelephant enemyCard:viking];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    BaseBattleStrategy *battleStrategy = warelephant.battleStrategy;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertFalse(viking.dead, @"Viking should survice attack");
        STAssertTrue(viking.hitpoints == 1, @"Viking should only have 1 hitpoint left");
        STAssertTrue(viking.cardLocation.row == 4, @"Viking should be pushed");
        STAssertTrue(viking.cardLocation.column == 3, @"Viking should be pushed");
    }];
}

- (void)testWarElephantKillsVikingIfPushIsNotPossible {
    
    WarElephant *warelephant = [WarElephant card];
    Viking *viking = [Viking card];
    Pikeman *pikeman = [Pikeman card];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    warelephant.cardColor = kCardColorGreen;
    
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    viking.cardColor = kCardColorRed;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObjects:viking, pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:warelephant enemyCard:viking];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    BaseBattleStrategy *battleStrategy = warelephant.battleStrategy;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue(viking.dead, @"Viking should be dead");
        STAssertTrue(viking.hitpoints == 0, @"Viking should be dead");
        STAssertFalse(pikeman.dead, @"Pikeman should survice");
    }];
}


- (void)testWarElephantHitsSurroundingEnemies {
    
    WarElephant *warelephant = [WarElephant card];
    Pikeman *pikeman = [Pikeman card];
    Pikeman *pikeman2 = [Pikeman card];
    Pikeman *pikeman3 = [Pikeman card];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    warelephant.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorRed;
    pikeman2.cardLocation = [GridLocation gridLocationWithRow:3 column:2];
    pikeman2.cardColor = kCardColorRed;
    pikeman3.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    pikeman3.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObjects:pikeman, pikeman2, pikeman3, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:warelephant enemyCard:pikeman];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    BaseBattleStrategy *battleStrategy = warelephant.battleStrategy;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 1;
    
    battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
    
    StandardBattleStrategy *aoeBattleStrategy = [StandardBattleStrategy strategy];

    FixedDiceStrategy *attackDiceStrategy = [FixedDiceStrategy strategy];
    attackDiceStrategy.fixedDieValue = 5;
    
    FixedDiceStrategy *defenderDiceStrategy = [FixedDiceStrategy strategy];
    defenderDiceStrategy.fixedDieValue = 5;

    aoeBattleStrategy.attackerDiceStrategy = attackDiceStrategy;
    aoeBattleStrategy.defenderDiceStrategy = defenderDiceStrategy;
    
    warelephant.aoeBattleStrategy = aoeBattleStrategy;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertTrue(pikeman.cardLocation.row == 4, @"Pikeman should be pushed");
        STAssertTrue(pikeman.cardLocation.column == 3, @"Pikeman should be pushed");
        
        STAssertTrue(pikeman2.dead, @"Pikeman2 should be dead");
        STAssertTrue(pikeman3.dead, @"Pikeman3 should be dead");
    }];
}

- (void)testWarElephantPushesVikingWithoutLossOfLifeIfVikingDefenseIsSuccessful {
    
    WarElephant *warelephant = [WarElephant card];
    Viking *viking = [Viking card];
    
    warelephant.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    warelephant.cardColor = kCardColorGreen;
    
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    viking.cardColor = kCardColorRed;
        
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:warelephant]
                                    player2Units:[NSArray arrayWithObject:viking]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:viking.cardLocation]] andCardInAction:warelephant enemyCard:viking];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    meleeAction.delegate = mock;
    
    BaseBattleStrategy *battleStrategy = warelephant.battleStrategy;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 2;
    
    battleStrategy.attackerDiceStrategy = _attackerFixedStrategy;
    battleStrategy.defenderDiceStrategy = _defenderFixedStrategy;
    
    [meleeAction performActionWithCompletion:^{
        
        STAssertFalse(viking.dead, @"Viking should be alive");
        STAssertTrue(viking.hitpoints == 2, @"Viking should still have 2 hitpoints");
        STAssertTrue(viking.cardLocation.row == 4, @"Viking should be pushed");
        STAssertTrue(viking.cardLocation.column == 3, @"Viking should be pushed");
    }];
}

- (void)testVikingShouldBeAbleToPerformMeleeActionWithoutConquerAgainstUnitsInRangeTwo {
    
    WarElephant *warelephant = [WarElephant card];
    Viking *viking = [Viking card];
    
    viking.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    viking.cardColor = kCardColorGreen;

    warelephant.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    warelephant.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:viking]
                                    player2Units:[NSArray arrayWithObject:warelephant]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    
    NSArray *meleeAactions = [pathFinder getMeleeAttackActionsFromLocation:viking.cardLocation forCard:viking enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeAactions.count == 1, @"Viking should be able to attack warelephant in range 2");

    MeleeAttackAction *action = meleeAactions[0];
    STAssertTrue(action.meleeAttackType == kMeleeAttackTypeNormal, @"Viking shouldn't be able to conquer warelephant");
}

- (void)testLongswordsmanCannotMoveAfterAttack {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];

    Samurai *samurai = [Samurai card];
    Pikeman *pikeman = [Pikeman card];
    Archer *archer = [Archer card];
    
    samurai.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    samurai.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    pikeman.cardColor = kCardColorRed;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:samurai]
                                    player2Units:[NSArray arrayWithObjects:pikeman, archer, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;

    PathFinder *pathfinder = [[PathFinder alloc ]init];
    MeleeAttackAction *action = [pathfinder getMeleeAttackActionForCard:samurai againstEnemyUnit:pikeman allLocations:_manager.currentGame.unitLayout];
    action.delegate = mock;
    
    samurai.battleStrategy = _battleStrategy;

    STAssertTrue(action.meleeAttackType == kMeleeAttackTypeConquer, @"Samurai should be able to attack&conquer pikeman");
    
    [action performActionWithCompletion:^{
        
        MeleeAttackAction *secondaryAttack = [pathfinder getMeleeAttackActionForCard:samurai againstEnemyUnit:archer allLocations:_manager.currentGame.unitLayout];
        
        STAssertNotNil(secondaryAttack, @"Samurai should be able to make a secondary attack");
        STAssertTrue(secondaryAttack.meleeAttackType == kMeleeAttackTypeNormal, @"Samurai shouldn't be able to attack&conquer archer");
    }];
}

- (void)testDiplomatSpecialAbility {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];

    Diplomat *diplomat = [Diplomat card];
    Pikeman *pikeman = [Pikeman card];
    
    diplomat.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    diplomat.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    pikeman.cardColor = kCardColorRed;
        
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:diplomat]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    PathFinder *pathfinder = [[PathFinder alloc ] init];
    NSArray *actions = [pathfinder getAbilityActionsFromLocation:diplomat.cardLocation
                                                         forCard:diplomat
                                                   friendlyUnits:_manager.currentGame.myDeck.cards
                                                      enemyUnits:_manager.currentGame.enemyDeck.cards
                                                    allLocations:_manager.currentGame.unitLayout];
    
    STAssertNotNil(actions, @"Diplomat should be able to bribe pikeman");
    
    AbilityAction *action = actions[0];
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        STAssertTrue(pikeman.cardColor == diplomat.cardColor, @"Pikeman should now be green");
        STAssertTrue([pikeman.attack calculateValue].lowerValue == 4, @"Pikeman should have +1A when bribed");
        
        [_manager endTurn];
        
        STAssertTrue(pikeman.cardColor == kCardColorRed, @"Pikeman should be red again");
        STAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikemans attackbonus from bribe should be gone");
        STAssertTrue([pikeman isAffectedByAbility:kAbilityCoolDown], @"Pikeman is affected by cooldown");
        
        [_manager endTurn];
        
        STAssertTrue([pikeman isAffectedByAbility:kAbilityCoolDown], @"Pikeman should no longer be affected by cooldown");
        
        [_manager endTurn];

        STAssertFalse([pikeman isAffectedByAbility:kAbilityCoolDown], @"Pikeman should no longer be affected by cooldown");
    }];
}

- (void)testJuggernautAlwaysPushedOnSuccessfulAttack {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Juggernaut *juggernaut = [Juggernaut card];
    Pikeman *pikeman = [Pikeman card];
    
    juggernaut.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    juggernaut.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:juggernaut]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:juggernaut enemyCard:pikeman meleeAttackType:kMeleeAttackTypeConquer];

    FixedDiceStrategy *attackerFixedStrategy = [FixedDiceStrategy strategyWithFixedValue:6];

    JuggernautBattleStrategy *battleStrategy = (JuggernautBattleStrategy*)[juggernaut newBattleStrategy];
    battleStrategy.attackerDiceStrategy = attackerFixedStrategy;
    
    action.delegate = mock;
    
    [action performActionWithCompletion:^{

        STAssertFalse(pikeman.dead, @"Pikeman should be alive");
        STAssertTrue([pikeman.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:3]], @"Pikeman should be pushed");
        STAssertTrue([juggernaut.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:4]], @"Juggernaut should have conquered pikemans location");
    }];
}

- (void)testJuggernautAlwaysPushedOnSuccessfulAttackKeepOriginalPositionWhenNotConquer {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Juggernaut *juggernaut = [Juggernaut card];
    Pikeman *pikeman = [Pikeman card];
    
    juggernaut.cardLocation = [GridLocation gridLocationWithRow:4 column:5];
    juggernaut.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:juggernaut]
                                    player2Units:[NSArray arrayWithObjects:pikeman, nil]];
    
    _manager.currentPlayersTurn = kPlayerGreen;
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithPath:@[[[PathFinderStep alloc] initWithLocation:pikeman.cardLocation]] andCardInAction:juggernaut enemyCard:pikeman meleeAttackType:kMeleeAttackTypeNormal];
    
    FixedDiceStrategy *attackerFixedStrategy = [FixedDiceStrategy strategyWithFixedValue:6];
    
    JuggernautBattleStrategy *battleStrategy = (JuggernautBattleStrategy*)[juggernaut newBattleStrategy];
    battleStrategy.attackerDiceStrategy = attackerFixedStrategy;
    
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        
        STAssertFalse(pikeman.dead, @"Pikeman should be alive");
        STAssertTrue([pikeman.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:3]], @"Pikeman should be pushed");
        STAssertTrue([juggernaut.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:4 column:5]], @"Juggernaut should have conquered pikemans location");
    }];
}


@end
