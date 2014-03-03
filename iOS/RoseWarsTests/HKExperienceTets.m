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
#import "LongSwordsMan.h"
#import "RoyalGuard.h"
#import "MeleeAttackAction.h"
#import "PathFinderStrategyFactory.h"
#import "FlagBearer.h"
#import "Catapult.h"
#import "RawBonus.h"
#import "RangeAttribute.h"
#import "Lancer.h"
#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"

@interface HKExperienceTets : XCTestCase

@property (nonatomic, strong) GameManager *manager;

@end

@implementation HKExperienceTets

- (void)setUp
{
    [super setUp];
    
    self.manager = [GameManager sharedManager];
}

- (void)tearDown
{
    [super tearDown];
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
    
    [_manager resolveCombatBetween:attacker defender:defender2 battleStrategy:attacker.battleStrategy];
    
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


@end
