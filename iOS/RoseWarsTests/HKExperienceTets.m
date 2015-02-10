//
//  HKExperienceTets.m
//  RoseWars
//
//  Created by Heine Kristensen on 02/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <XCTest/XCTest.h>
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
#import "Lancer.h"
#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"
#import "MoveAction.h"
#import "AbilityAction.h"
#import "RangedAttackAction.h"
#import "Weaponsmith.h"
#import "Samurai.h"

@interface HKExperienceTets : XCTestCase

@property (nonatomic, strong) GameManager *gamemanager;

@end

@implementation HKExperienceTets

- (void)setUp
{
    [super setUp];
    
    self.gamemanager = [[GameManager alloc] init];
}

- (void)tearDown
{
    [super tearDown];
}

- (void)testAnyActionTypePerformedAwardsExperiencePoints {
    
    Archer *archer = [Archer card];
    Pikeman *pikeman = [Pikeman card];
    LightCavalry *cavalry = [LightCavalry card];
    Weaponsmith *weaponsmith = [Weaponsmith card];
    Archer *enemy = [Archer card];
    Archer *enemy2 = [Archer card];
    
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    archer.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    pikeman.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    cavalry.cardLocation = [GridLocation gridLocationWithRow:5 column:3];
    cavalry.cardColor = kCardColorGreen;
    weaponsmith.cardLocation = [GridLocation gridLocationWithRow:3 column:4];
    enemy.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    enemy.cardColor = kCardColorRed;
    enemy2.cardLocation = [GridLocation gridLocationWithRow:5 column:4];
    enemy2.cardColor = kCardColorRed;
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObjects:archer, pikeman, cavalry, weaponsmith, nil]
                                    player2Units:[NSArray arrayWithObjects:enemy, enemy2, nil]];

    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];

    NSArray *moveActions = [pathfinder getMoveActionsFromLocation:pikeman.cardLocation forCard:pikeman enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    XCTAssertTrue(moveActions.count > 0, @"Cavalry should be able to move");
    MoveAction *moveAction = moveActions[0];
    moveAction.delegate = mock;
    [moveAction performActionWithCompletion:^{
        XCTAssertTrue(pikeman.experience == 1, @"Pikeman should have been awarded an experience point by moving");
    }];
    
    NSArray *rangedActions = [pathfinder getRangedAttackActionsFromLocation:archer.cardLocation forCard:archer enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    XCTAssertTrue(rangedActions.count > 0, @"Archer should be able to attack");
    RangedAttackAction *rangedAction = rangedActions[0];
    rangedAction.delegate = mock;
    [rangedAction performActionWithCompletion:^{
        XCTAssertTrue(archer.experience == 1, @"Archer should be awarded an experience point by attacking");
    }];
    
    // Reset move counters
    [self.gamemanager endTurn];
    [self.gamemanager endTurn];
    
    NSArray *abilityActions = [pathfinder getAbilityActionsFromLocation:weaponsmith.cardLocation forCard:weaponsmith friendlyUnits:self.gamemanager.currentGame.myDeck.cards enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    AbilityAction *abilityAction = abilityActions[0];
    abilityAction.delegate = mock;
    [abilityAction performActionWithCompletion:^{
        XCTAssertTrue(weaponsmith.experience == 1, @"Weaponsmith should be awarded an experience point for using ability");
    }];
    
    MeleeAttackAction *meleeAction = [pathfinder getMeleeAttackActionForCard:cavalry againstEnemyUnit:enemy2 allLocations:self.gamemanager.currentGame.unitLayout];
    meleeAction.delegate = mock;
    [meleeAction performActionWithCompletion:^{
        XCTAssertTrue(cavalry.experience == 1, @"Cavalry should be awarded an experience point by attacking");
    }];
}

- (void)testOnlyOneExperiecePointPerRound {
    
    Samurai *attacker = [Samurai card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:4 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender1.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:1];

    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    MeleeAttackAction *attack = [pathfinder getMeleeAttackActionForCard:attacker againstEnemyUnit:defender1 allLocations:self.gamemanager.currentGame.unitLayout];
    GameBoardMockup *mock = [GameBoardMockup new];
    attack.delegate = mock;
    XCTAssertNotNil(attack, @"Samurai should be able to attack");

    [attack performActionWithCompletion:^{
        XCTAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");
        
        MeleeAttackAction *attack = [pathfinder getMeleeAttackActionForCard:attacker againstEnemyUnit:defender1 allLocations:self.gamemanager.currentGame.unitLayout];
        XCTAssertNotNil(attack, @"Samurai should be able to attack");
        attack.delegate = mock;
        [attack performActionWithCompletion:^{
            XCTAssertTrue(attacker.experience == 1, @"Attacker should not have gained extra XP this round");
        }];
    }];
}

- (void)testUnitShouldIncreaseInLevelAfterPerformingFourActions {
    
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    
    attacker.cardLocation = [GridLocation gridLocationWithRow:3 column:3];
    defender1.cardLocation = [GridLocation gridLocationWithRow:6 column:3];
    
    self.gamemanager.currentGame = [TestHelper setupGame:self.gamemanager.currentGame gamemanager:self.gamemanager
                                withPlayer1Units:[NSArray arrayWithObject:attacker]
                                    player2Units:[NSArray arrayWithObjects:defender1, nil]];
    
    attacker.battleStrategy.attackerDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:5];
    defender1.battleStrategy.defenderDiceStrategy = [FixedDiceStrategy strategyWithFixedValue:1];

    XCTAssertTrue(attacker.numberOfLevelsIncreased == 0, @"Card shouldn't have increased in level");
    
    PathFinder *pathfinder = [[PathFinder alloc] initWithGameManager:self.gamemanager];
    GameBoardMockup *mock = [[GameBoardMockup alloc] init];
    
    NSArray *actions = [pathfinder getRangedAttackActionsFromLocation:attacker.cardLocation forCard:attacker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
    XCTAssertTrue(actions.count == 1, @"Archer should be able to attack");
    RangedAttackAction *attack = actions[0];
    attack.delegate = mock;
    [attack performActionWithCompletion:^{
        XCTAssertTrue(attacker.experience == 1, @"Should have gained 1 xp");
        [self.gamemanager endTurn];

        NSArray *actions = [pathfinder getRangedAttackActionsFromLocation:attacker.cardLocation forCard:attacker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
        XCTAssertTrue(actions.count == 1, @"Archer should be able to attack");
        RangedAttackAction *attack = actions[0];
        attack.delegate = mock;
        [attack performActionWithCompletion:^{
            XCTAssertTrue(attacker.experience == 2, @"Should have gained 2 xp");
            [self.gamemanager endTurn];

            NSArray *actions = [pathfinder getRangedAttackActionsFromLocation:attacker.cardLocation forCard:attacker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
            XCTAssertTrue(actions.count == 1, @"Archer should be able to attack");
            RangedAttackAction *attack = actions[0];
            attack.delegate = mock;
            [attack performActionWithCompletion:^{
                XCTAssertTrue(attacker.experience == 3, @"Should have gained 3 xp");
                [self.gamemanager endTurn];

                NSArray *actions = [pathfinder getRangedAttackActionsFromLocation:attacker.cardLocation forCard:attacker enemyUnits:self.gamemanager.currentGame.enemyDeck.cards allLocations:self.gamemanager.currentGame.unitLayout];
                XCTAssertTrue(actions.count == 1, @"Archer should be able to attack");
                RangedAttackAction *attack = actions[0];
                attack.delegate = mock;
                [attack performActionWithCompletion:^{
                    XCTAssertTrue(attacker.experience == 4, @"Should have increased in level");
                    XCTAssertTrue(attacker.numberOfLevelsIncreased == 1, @"Should have increased in level");
                }];
            }];
        }];
    }];
}


@end
