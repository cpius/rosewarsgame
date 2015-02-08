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
#import "Longswordsman.h"
#import "RoyalGuard.h"
#import "MeleeAttackAction.h"
#import "PathFinderStrategyFactory.h"
#import "FlagBearer.h"
#import "Catapult.h"
#import "RawBonus.h"
#import "RangeAttribute.h"
#import "Lancer.h"
#import "CardPool.h"

@interface CombatTest()

@property (nonatomic) GameManager *gamemanager;

@end

@implementation CombatTest

- (void)setUp
{
    [super setUp];

    self.gamemanager = [[GameManager alloc] init];
}

- (void)testSimpleCombatDefenceSucces {
    
    Archer *attacker = [CardPool createCardOfName:kArcher withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender, nil]];
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:1];
    
    BattleResult *outcome = [self.gamemanager resolveCombatBetween:attacker defender:defender battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(IsDefenseSuccessful(outcome.combatOutcome), @"Pike should have defended successfully");

    XCTAssertTrue(!defender.dead, @"Defender isn't dead");
    XCTAssertTrue(!attacker.dead, @"Attacker isn't dead");
}

- (void)testSimpleCombatAttackSucces {
    
    Archer *attacker = [CardPool createCardOfName:kArcher withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender, nil]];
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:4];
    
    BattleResult *outcome = [self.gamemanager resolveCombatBetween:attacker defender:defender battleStrategy:attacker.battleStrategy];
    
    XCTAssertTrue(IsAttackSuccessful(outcome.combatOutcome), @"Attack should be successful");
    
    XCTAssertTrue(defender.dead, @"Defender is dead");
    XCTAssertTrue(!attacker.dead, @"Attacker isn't dead");
}


- (void)testTimedBonusShouldDisappear {
    
    Archer *attacker = [CardPool createCardOfName:kArcher withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];

    TimedBonus *timedBonus = [[TimedBonus alloc] initWithValue:2 forNumberOfTurns:2 gamemanager:self.gamemanager];
    [attacker.attack addTimedBonus:timedBonus];
    
    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 3, @"Attack lower value should be 3");
    
    [self.gamemanager endTurn];
    [self.gamemanager endTurn];

    XCTAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Attack lower value should be 5");
}

- (void)testAttackDirections {
    
    LightCavalry *attacker = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    BattlePlan *battlePlan = [[BattlePlan alloc] initWithGame:self.gamemanager];
    PathFinder *pathFinder = [[PathFinder alloc ] initWithGameManager:self.gamemanager];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender1.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:self.gamemanager.currentGame.unitLayout];
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:path[0] andCardInAction:attacker enemyCard:defender1];
    
    NSDictionary *attackDirections = [battlePlan getAttackDirectionsAction:meleeAction withUnitLayout:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(attackDirections.count == 4, @"Should be 4 attackdirections");

    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:2]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:3]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:4]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:5 column:3]], @"Should be an attackdirection");
}

- (void)testAttackDirectionsWithEnemyCardsObstructing {
    
    LightCavalry *attacker = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *defender1 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *defender2 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Archer *defender3 = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    defender2.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    defender3.cardLocation = [GridLocation gridLocationWithRow:5 column:2];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, defender2, defender3, nil]];
    
    BattlePlan *battlePlan = [[BattlePlan alloc] initWithGame:self.gamemanager];
    PathFinder *pathFinder = [[PathFinder alloc ] initWithGameManager:self.gamemanager];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender2.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:self.gamemanager.currentGame.unitLayout];
        
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:path[0] andCardInAction:attacker enemyCard:defender2];
    
    NSDictionary *attackDirections = [battlePlan getAttackDirectionsAction:meleeAction withUnitLayout:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(attackDirections.count == 3, @"Should be 3 attackdirections");
    
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:2]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:4]], @"Should be an attackdirection");
    XCTAssertNotNil([attackDirections objectForKey:[GridLocation gridLocationWithRow:4 column:3]], @"Should be an attackdirection");
}

- (void)testAttackDirectionsWithBerserker {
    
    Berserker *attacker = [CardPool createCardOfName:kBerserker withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender1 = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:5 column:3];

    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    BattlePlan *battlePlan = [[BattlePlan alloc] initWithGame:self.gamemanager];
    PathFinder *pathFinder = [[PathFinder alloc ] initWithGameManager:self.gamemanager];
    
    NSArray *path = [pathFinder getPathForCard:attacker fromGridLocation:attacker.cardLocation toGridLocation:defender1.cardLocation usingStrategy:[PathFinderStrategyFactory getMeleeAttackStrategy] allLocations:self.gamemanager.currentGame.unitLayout];
    
    MeleeAttackAction *meleeAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:path[0] andCardInAction:attacker enemyCard:defender1];
    
    NSDictionary *attackDirections = [battlePlan getAttackDirectionsAction:meleeAction withUnitLayout:self.gamemanager.currentGame.unitLayout];
    
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
    
    Longswordsman *longswordsman = [CardPool createCardOfName:kLongswordsman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    RoyalGuard *royalguard = [CardPool createCardOfName:kRoyalGuard withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    longswordsman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    royalguard.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:2 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:longswordsman]
                                    player2Units:[NSArray arrayWithObjects:royalguard, pikeman, nil]];
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    NSArray *meleeActions = [pathFinder getMeleeAttackActionsFromLocation:longswordsman.cardLocation forCard:longswordsman enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
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
    
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    FlagBearer *flagbearer = [CardPool createCardOfName:kFlagBearer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:flagbearer]
                                    player2Units:[NSArray arrayWithObjects:archer, pikeman, nil]];
    
    PathFinder *pathFinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    NSArray *meleeActions = [pathFinder getMeleeAttackActionsFromLocation:flagbearer.cardLocation forCard:flagbearer enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(meleeActions.count == 1, @"FlagBearer should only be able to attack pikeman");
}

- (void)testStandardBattleStrategyWhenAffectedByFlagBearer {
    
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    FlagBearer *flagbearer = [CardPool createCardOfName:kFlagBearer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    pikeman.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:5 column:4];
    defender.cardLocation = [GridLocation gridLocationWithRow:4 column:3];

    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:flagbearer, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:defender]];
    
    pikeman.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:4];
    defender.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:[GridLocation gridLocationWithRow:4 column:3]];
    MeleeAttackAction *attackAction = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[step] andCardInAction:pikeman enemyCard:defender];
    
    attackAction.delegate = mock;
    
    [attackAction performActionWithCompletion:^{
        XCTAssertTrue(defender.dead, @"Defender should be dead");
        XCTAssertTrue(attackAction.battleResult.combatOutcome == kCombatOutcomeAttackSuccessful, @"Attack should be succesful");
    }];
}

- (void)testUnitIsntAffectedByAoeEffectFromDeadFlagBearer {
    
    FlagBearer *flagbearer = [CardPool createCardOfName:kFlagBearer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *defender = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    flagbearer.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    flagbearer.dead = YES;
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender.cardLocation = [GridLocation gridLocationWithRow:4 column:4];

    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:flagbearer, pikeman, nil]
                                    player2Units:[NSArray arrayWithObject:defender]];
    
    PathFinderStep *step = [[PathFinderStep alloc] initWithLocation:defender.cardLocation];
    
    MeleeAttackAction *action = [[MeleeAttackAction alloc] initWithGameManager:self.gamemanager path:@[step] andCardInAction:pikeman enemyCard:defender];
    
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
    
    Catapult *catapult = [CardPool createCardOfName:kCatapult withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    catapult.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:catapult]
                                    player2Units:[NSArray arrayWithObject:pikeman]];
    
    [catapult.attack addRawBonus:[[RawBonus alloc] initWithValue:1]];

    catapult.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    
    // Even though Pikeman defense is succesfull, because of the catapult +1A, pikemans defense is lowered by 1
    pikeman.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:3];
    
    BattleResult *result = [self.gamemanager resolveCombatBetween:catapult defender:pikeman battleStrategy:catapult.battleStrategy];
    
    XCTAssertTrue(result.combatOutcome == kCombatOutcomeAttackSuccessful, @"Catapul attack should be succesfull");
    XCTAssertTrue(pikeman.dead, @"Pikeman should be dead");
}

// TODO: Skal afklares! Burde lightcavalry ikke kunne angribe archer uden conquer?
- (void)testCavalryCanAttackButNotConquerEnemyWhileInZoneOfControl {
    
    LightCavalry *lightCavalry = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    Pikeman *pikeman = [CardPool createCardOfName:kPikeman withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    lightCavalry.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    archer.cardLocation = [GridLocation gridLocationWithRow:3 column:2];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager withPlayer1Units:@[lightCavalry] player2Units:@[archer, pikeman]];
    
    PathFinder *finder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    NSArray *actions = [finder getMeleeAttackActionsFromLocation:lightCavalry.cardLocation forCard:lightCavalry enemyUnits:@[archer, pikeman] allLocations:self.gamemanager.currentGame.unitLayout];
}

- (void)testLightCavalryCanAttackArcherFromThreeDirections {
    LightCavalry *lightCavalry = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    Archer *archer = [CardPool createCardOfName:kArcher withCardColor:kCardColorRed gamemanager:self.gamemanager];
    
    lightCavalry.cardLocation = [GridLocation gridLocationWithRow:4 column:2];
    archer.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager withPlayer1Units:@[lightCavalry] player2Units:@[archer]];
    
    BattlePlan *battleplan = [[BattlePlan alloc] initWithGame:self.gamemanager];
    [battleplan createBattlePlanForCard:lightCavalry friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards unitLayout:self.gamemanager.currentGame.unitLayout];
  
    XCTAssertTrue(battleplan.meleeActions.count == 1, @"LightCavalry should be able to attack archer");
    
    MeleeAttackAction *action = battleplan.meleeActions[0];
    NSDictionary *attackDirections = [battleplan getAttackDirectionsAction:action withUnitLayout:self.gamemanager.currentGame.unitLayout];
    
    XCTAssertTrue(attackDirections.count == 3, @"LightCavalry should be able to attack archer from 3 directions");
}

- (void)testLancerCanConquerEnemy {
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    Lancer *lancer = [CardPool createCardOfName:kLancer withCardColor:kCardColorGreen gamemanager:self.gamemanager];
    lancer.cardLocation = [GridLocation gridLocationWithRow:5 column:2];
    lancer.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:6];
    
    LightCavalry *cavalry = [CardPool createCardOfName:kLightCavalry withCardColor:kCardColorRed gamemanager:self.gamemanager];
    cavalry.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    cavalry.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:6];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager withPlayer1Units:@[lancer] player2Units:@[cavalry]];
    
    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    MeleeAttackAction *action = [pathfinder getMeleeAttackActionForCard:lancer againstEnemyUnit:cavalry allLocations:self.gamemanager.currentGame.unitLayout];
    action.delegate = mock;
    
    [action performActionWithCompletion:^{
        [action conquerEnemyLocationWithCompletion:^{
            XCTAssertTrue([lancer.cardLocation isSameLocationAs:[GridLocation gridLocationWithRow:3 column:3]], @"Lancer should have conquered cavalry. Actual location: %@", lancer.cardLocation);
        }];
    }];
    
    XCTAssertTrue(action != nil, @"Lancer should be able to attack lightcavalry");
}

@end
