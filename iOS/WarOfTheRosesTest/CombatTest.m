//
//  CombatTest.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import "CombatTest.h"
#import "Definitions.h"
#import "GridLocation.h"
#import "Archer.h"
#import "PathFinder.h"
#import "Pikeman.h"
#import "LightCavalry.h"
#import "TestHelper.h"
#import "TimedBonus.h"
#import "StandardBattleStrategy.h"
#import "GameManager.h"
#import "BattleResult.h"
#import "Berserker.h"
#import "LongSwordsMan.h"
#import "RoyalGuard.h"
#import "MeleeAttackAction.h"
#import "PathFinderStrategyFactory.h"
#import "FlagBearer.h"

@implementation CombatTest

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

- (void)testSimpleCombatDefenceSucces {
    
    Archer *attacker = [Archer card];
    Pikeman *defender = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender, nil]];
    
    _attackerFixedStrategy.fixedDieValue = 3;
    _defenderFixedStrategy.fixedDieValue = 1;
    
    BattleResult *outcome = [_manager resolveCombatBetween:attacker defender:defender battleStrategy:_battleStrategy];
    
    STAssertTrue(IsDefenseSuccessful(outcome.combatOutcome), @"Pike should have defended successfully");

    STAssertTrue(!defender.dead, @"Defender isn't dead");
    STAssertTrue(!attacker.dead, @"Attacker isn't dead");
}

- (void)testSimpleCombatAttackSucces {
    
    Archer *attacker = [Archer card];
    Pikeman *defender = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender, nil]];
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 4;
    
    BattleResult *outcome = [_manager resolveCombatBetween:attacker defender:defender battleStrategy:_battleStrategy];
    
    STAssertTrue(IsAttackSuccessful(outcome.combatOutcome), @"Attack should be successful");
    
    STAssertTrue(defender.dead, @"Defender is dead");
    STAssertTrue(!attacker.dead, @"Attacker isn't dead");
}

- (void)testOnlyOneExperiecePointPerRound {
        
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    LightCavalry *defender2 = [LightCavalry card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender2.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, nil]];
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    [_manager resolveCombatBetween:attacker defender:defender1 battleStrategy:_battleStrategy];
    
    STAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");

    [_manager resolveCombatBetween:attacker defender:defender2 battleStrategy:_battleStrategy];

    STAssertTrue(attacker.experience == 1, @"Attacker should not have gained extra XP this round");
}

- (void)testUnitShouldIncreaseInLevelAfterTwoSuccesfulAttacksOverTwoRounds {
        
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    LightCavalry *defender2 = [LightCavalry card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    defender2.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, nil]];

    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    [_manager resolveCombatBetween:attacker defender:defender1 battleStrategy:_battleStrategy];
    
    STAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");
    
    [_manager endTurn];
    
    [_manager resolveCombatBetween:attacker defender:defender2 battleStrategy:_battleStrategy];
    
    STAssertTrue(attacker.experience == 2, @"Attacker should have gained 2 XP");
    STAssertTrue(attacker.numberOfLevelsIncreased == 1, @"Attacker should have increased a level");
}

- (void)testTimedBonusShouldDisappear {
    
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];

    TimedBonus *timedBonus = [[TimedBonus alloc] initWithValue:2 forNumberOfTurns:2];
    [attacker.attack addTimedBonus:timedBonus];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 3, @"Attack lower value should be 3");
    
    [_manager endTurn];
    [_manager endTurn];

    STAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Attack lower value should be 5");
}

- (void)testAttackDirections {
    
    LightCavalry *attacker = [LightCavalry card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    BattlePlan *battlePlan = [[BattlePlan alloc] init];
    PathFinder *pathFinder = [[PathFinder alloc ] init];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender1.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:_manager.currentGame.unitLayout];
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:path[0] andCardInAction:attacker enemyCard:defender1];
    
    NSDictionary *attackDirections = [battlePlan getAttackDirectionsAction:meleeAction withUnitLayout:_manager.currentGame.unitLayout];
    
    STAssertTrue(attackDirections.count == 3, @"Should be 3 attackdirections");

    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:2]], @"Should be an attackdirection");
    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:3]], @"Should be an attackdirection");
    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
}

- (void)testAttackDirectionsWithEnemyCardsObstructing {
    
    LightCavalry *attacker = [LightCavalry card];
    Pikeman *defender1 = [Pikeman card];
    Pikeman *defender2 = [Pikeman card];
    Pikeman *defender3 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    defender2.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    defender3.cardLocation = [GridLocation gridLocationWithRow:5 column:2];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    BattlePlan *battlePlan = [[BattlePlan alloc] init];
    PathFinder *pathFinder = [[PathFinder alloc ] init];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender1.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:_manager.currentGame.unitLayout];
        
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:path[0] andCardInAction:attacker enemyCard:defender1];
    
    NSDictionary *attackDirections = [battlePlan getAttackDirectionsAction:meleeAction withUnitLayout:_manager.currentGame.unitLayout];
    
    STAssertTrue(attackDirections.count == 1, @"Should be 1 attackdirections");
    
    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
}

- (void)testAttackDirectionsWithBerserker {
    
    Berserker *attacker = [Berserker card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    attacker.cardColor = kCardColorGreen;
    
    defender1.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    defender1.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    BattlePlan *battlePlan = [[BattlePlan alloc] init];
    PathFinder *pathFinder = [[PathFinder alloc ] init];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender1.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:_manager.currentGame.unitLayout];
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithPath:path[0] andCardInAction:attacker enemyCard:defender1];
    
    NSDictionary *attackDirections = [battlePlan getAttackDirectionsAction:meleeAction withUnitLayout:_manager.currentGame.unitLayout];
    
    STAssertTrue(attackDirections.count == 3, @"Should be 3 attackdirections");
    
    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:2]], @"Should be an attackdirection");
    STAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:3]], @"Should be an attackdirection");
}

- (void)testDefenseCannotExceedFour {
    
    Berserker *attacker = [Berserker card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    attacker.cardColor = kCardColorGreen;
    
    [attacker.defence addRawBonus:[[RawBonus alloc] initWithValue:4]];
    
    STAssertTrue([attacker.defence calculateValue].upperValue == 4, @"Defense upper value should be 4");
}

- (void)testLongswordsManCanAttackEnemyUnitWhenStandingNextToRoyalGuardButNotConquer {
    
    LongSwordsMan *longswordsman = [LongSwordsMan card];
    RoyalGuard *royalguard = [RoyalGuard card];
    Pikeman *pikeman = [Pikeman card];
    
    longswordsman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    longswordsman.cardColor = kCardColorGreen;
    
    royalguard.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    royalguard.cardColor = kCardColorRed;

    pikeman.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:longswordsman]
                                    player2Units:[NSArray arrayWithObjects:royalguard, pikeman, nil]];
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    NSArray *meleeActions = [pathFinder getMeleeAttackActionsFromLocation:longswordsman.cardLocation forCard:longswordsman enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeActions.count == 2, @"Longswordsman should be able to attack royalguard and pikeman");
    
    for (MeleeAttackAction *action in meleeActions) {
        if (action.enemyCard == pikeman) {
            STAssertTrue(action.meleeAttackType == kMeleeAttackTypeNormal, @"Longswordsman shouldn't be able to conquer pikeman");
        }
        
        if (action.enemyCard == royalguard) {
            STAssertTrue(action.meleeAttackType == kMeleeAttackTypeConquer, @"Longswordsman should be able to conquer royalguard");
        }
    }
}

- (void)testUnitNotAffectedByZocWhenMakingNormalMeleeAttackWithoutConquer {
    
    Archer *archer = [Archer card];
    FlagBearer *flagbearer = [FlagBearer card];
    Pikeman *pikeman = [Pikeman card];
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    flagbearer.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    archer.cardColor = kCardColorRed;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:flagbearer]
                                    player2Units:[NSArray arrayWithObjects:archer, pikeman, nil]];
    
    PathFinder *pathFinder = [[PathFinder alloc] init];
    NSArray *meleeActions = [pathFinder getMeleeAttackActionsFromLocation:flagbearer.cardLocation forCard:flagbearer enemyUnits:_manager.currentGame.enemyDeck.cards allLocations:_manager.currentGame.unitLayout];
    
    STAssertTrue(meleeActions.count == 1, @"FlagBearer should only be able to attack pikeman");
}



@end
