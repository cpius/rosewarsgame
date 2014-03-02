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
#import "GameBoardMockup.h"
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
#import "Catapult.h"
#import "RawBonus.h"
#import "RangeAttribute.h"
#import "Lancer.h"

@implementation CombatTest

- (void)setUp
{
    [super setUp];

    _manager = [GameManager sharedManager];
}

- (void)testSimpleCombatDefenceSucces {
    
    Archer *attacker = [Archer card];
    Pikeman *defender = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender, nil]];
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:1];
    
    BattleResult *outcome = [_manager resolveCombatBetween:attacker defender:defender battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(IsDefenseSuccessful(outcome.combatOutcome), @"Pike should have defended successfully");

    XCTAssertTrue(!defender.dead, @"Defender isn't dead");
    XCTAssertTrue(!attacker.dead, @"Attacker isn't dead");
}

- (void)testSimpleCombatAttackSucces {
    
    Archer *attacker = [Archer card];
    Pikeman *defender = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender, nil]];
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:4];
    
    BattleResult *outcome = [_manager resolveCombatBetween:attacker defender:defender battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(IsAttackSuccessful(outcome.combatOutcome), @"Attack should be successful");
    
    XCTAssertTrue(defender.dead, @"Defender is dead");
    XCTAssertTrue(!attacker.dead, @"Attacker isn't dead");
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
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender1.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    [_manager resolveCombatBetween:attacker defender:defender1 battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");

    [_manager resolveCombatBetween:attacker defender:defender2 battleStrategy:_battleStrategy];

    XCTAssertTrue(attacker.experience == 1, @"Attacker should not have gained extra XP this round");
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

    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender1.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender2.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    [_manager resolveCombatBetween:attacker defender:defender1 battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");
    
    [_manager endTurn];
    
    [_manager resolveCombatBetween:attacker defender:defender2 battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(attacker.experience == 2, @"Attacker should have gained 2 XP");
    XCTAssertTrue(attacker.numberOfLevelsIncreased == 1, @"Attacker should have increased a level");
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
    
    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 3, @"Attack lower value should be 3");
    
    [_manager endTurn];
    [_manager endTurn];

    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Attack lower value should be 5");
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
    
    XCTAssertTrue(attackDirections.count == 4, @"Should be 4 attackdirections");

    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:2]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:3]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:3]], @"Should be an attackdirection");
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
    
    XCTAssertTrue(attackDirections.count == 2, @"Should be 1 attackdirections");
    
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:3]], @"Should be an attackdirection");
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
    
    XCTAssertTrue(attackDirections.count == 4, @"Should be 4 attackdirections");
    
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:2]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:3]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:3]], @"Should be an attackdirection");
}

- (void)testDefenseCannotExceedFour {
    
    Berserker *attacker = [Berserker card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    attacker.cardColor = kCardColorGreen;
    
    [attacker.defence addRawBonus:[[RawBonus alloc] initWithValue:4]];
    
    XCTAssertTrue([attacker.defence calculateValue].upperValue == 4, @"Defense upper value should be 4");
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
    
    XCTAssertTrue(meleeActions.count == 2, @"Longswordsman should be able to attack royalguard and pikeman");
    
    for (MeleeAttackAction *action in meleeActions) {
        if (action.enemyCard == pikeman) {
            XCTAssertTrue(action.meleeAttackType == kMeleeAttackTypeNormal, @"Longswordsman shouldn't be able to conquer pikeman");
        }
        
        if (action.enemyCard == royalguard) {
            XCTAssertTrue(action.meleeAttackType == kMeleeAttackTypeConquer, @"Longswordsman should be able to conquer royalguard");
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
    
    XCTAssertTrue(meleeActions.count == 1, @"FlagBearer should only be able to attack pikeman");
}

- (void)testStandardBattleStrategyWhenAffectedByFlagBearer {
    
    Pikeman *pikeman = [Pikeman card];
    FlagBearer *flagbearer = [FlagBearer card];
    Pikeman *defender = [Pikeman card];
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    pikeman.cardColor = kCardColorGreen;
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:5 column:4];
    flagbearer.cardColor = kCardColorGreen;
    
    defender.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    defender.cardColor = kCardColorRed;

    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObjects:flagbearer, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:defender]];
    
    pikeman.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:4];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:4 column:3]];
    MeleeAttackAction *attackAction = [[MeleeAttackAction alloc] initWithPath:@[step] andCardInAction:pikeman enemyCard:defender];
    
    attackAction.delegate = mock;
    
    [attackAction performActionWithCompletion:^{
       
        XCTAssertTrue(defender.dead, @"Defender should be dead");
        XCTAssertTrue(attackAction.battleResult.combatOutcome == kCombatOutcomeAttackSuccessful, @"Attack should be succesful");
    }];
}

- (void)testUnitIsntAffectedByAoeEffectFromDeadFlagBearer {
    
    FlagBearer *flagbearer = [FlagBearer card];
    Pikeman *pikeman = [Pikeman card];
    Pikeman *defender = [Pikeman card];
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    flagbearer.cardColor = kCardColorGreen;
    flagbearer.dead = YES;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardColor = kCardColorGreen;
    
    defender.cardLocation = [GridLocation gridLocationWithRow:4 column:4];
    defender.cardColor = kCardColorRed;

    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObjects:flagbearer, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:defender]];
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:defender.cardLocation];
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithPath:@[step] andCardInAction:pikeman enemyCard:defender];
    
    pikeman.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:4];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    action.delegate = mock;

    [action performActionWithCompletion:^{
        
        XCTAssertFalse(defender.dead, @"Defender shouldn't be dead");
        XCTAssertTrue([pikeman.attack calculateValue].lowerValue == 5, @"Pikeman shouldn't receive bonus from dead flagbearer");
    }];
}

- (void)testUnitWithNoDefenseIsAlwaysKilledWhenAttackRollIsSuccesfull {
    
    // TODO
}

- (void)testUnitWithAttackLowerThanOneSubtractsOneFromDefendingUnitsDefense {
    
    Catapult *catapult = [Catapult card];
    Pikeman *pikeman = [Pikeman card];
    
    catapult.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    catapult.cardColor = kCardColorGreen;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame
                                withPlayer1Units:[NSArray arrayWithObject:catapult]
                                    player2Units:[NSArray arrayWithObject:pikeman]];
    
    [catapult.attack addRawBonus:[[RawBonus alloc] initWithValue:1]];

    catapult.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    
    // Even though Pikeman defense is succesfull, because of the catapult +1A, pikemans defense is lowered by 1
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    
    BattleResult *result = [_manager resolveCombatBetween:catapult defender:pikeman battleStrategy:catapult.battleStrategy];
    
    XCTAssertTrue(result.combatOutcome == kCombatOutcomeAttackSuccessful, @"Catapul attack should be succesfull");
    XCTAssertTrue(pikeman.dead, @"Pikeman should be dead");
}

// TODO: Skal afklares! Burde lightcavalry ikke kunne angribe archer uden conquer?
- (void)testCavalryCanAttackButNotConquerEnemyWhileInZoneOfControl {
    
    LightCavalry *lightCavalry = [LightCavalry card];
    Archer *archer = [Archer card];
    Pikeman *pikeman = [Pikeman card];
    
    lightCavalry.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    lightCavalry.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:2];
    archer.cardColor = kCardColorRed;
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    pikeman.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame withPlayer1Units:@[lightCavalry] player2Units:@[archer, pikeman]];
    
    PathFinder *finder = [[PathFinder alloc] init];
    NSArray *actions = [finder getMeleeAttackActionsFromLocation:lightCavalry.cardLocation forCard:lightCavalry enemyUnits:@[archer, pikeman] allLocations:_manager.currentGame.unitLayout];
}

- (void)testLightCavalryCanAttackArcherFromThreeDirections {
    
    LightCavalry *lightCavalry = [LightCavalry card];
    Archer *archer = [Archer card];
    
    lightCavalry.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    lightCavalry.cardColor = kCardColorGreen;
    
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    archer.cardColor = kCardColorRed;
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame withPlayer1Units:@[lightCavalry] player2Units:@[archer]];
    
    BattlePlan *battleplan = [[BattlePlan alloc] init];
    [battleplan createBattlePlanForCard:lightCavalry friendlyUnits:_manager.currentGame.myDeck.cards enemyUnits:_manager.currentGame.enemyDeck.cards unitLayout:_manager.currentGame.unitLayout];
  
    XCTAssertTrue(battleplan.meleeActions.count == 1, @"LightCavalry should be able to attack archer");
    
    MeleeAttackAction *action = battleplan.meleeActions[0];
    NSDictionary *attackDirections = [battleplan getAttackDirectionsAction:action withUnitLayout:_manager.currentGame.unitLayout];
    
    XCTAssertTrue(attackDirections.count == 3, @"LightCavalry should be able to attack archer from 3 directions");
}

- (void)testLancerCanConquerEnemy {
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Lancer *lancer = [Lancer card];
    lancer.cardLocation = [GridLocation gridLocationWithRow:5 column:2];
    lancer.cardColor = kCardColorGreen;
    lancer.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:6];

    
    LightCavalry *cavalry = [LightCavalry card];
    cavalry.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    cavalry.cardColor = kCardColorRed;
    cavalry.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:6];
    
    _manager.currentGame = [TestHelper setupGame:_manager.currentGame withPlayer1Units:@[lancer] player2Units:@[cavalry]];
    
    PathFinder *pathfinder = [[PathFinder alloc] init];
    MeleeAttackAction *action = [pathfinder getMeleeAttackActionForCard:lancer againstEnemyUnit:cavalry allLocations:_manager.currentGame.unitLayout];
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        [action conquerEnemyLocationWithCompletion:^{
            XCTAssertTrue([lancer.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:3 column:3]], @"Lancer should have conquered cavalry. Actual location: %@", lancer.cardLocation);
        }];
    }];
    
    XCTAssertTrue(action != nil, @"Lancer should be able to attack lightcavalry");
    
    
    
}

@end
