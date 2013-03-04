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
#import "Pikeman.h"
#import "LightCavalry.h"
#import "GameManager.h"
#import "TestHelper.h"
#import "TimedBonus.h"

@implementation CombatTest

- (void)setUp
{
    [super setUp];

    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
      
    _manager.attackerDiceStrategy = _attackerFixedStrategy;
    _manager.defenderDiceStrategy = _defenderFixedStrategy;
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
    
    CombatOutcome outcome = [_manager resolveCombatBetween:attacker defender:defender];
    
    STAssertTrue(IsDefenseSuccessful(outcome), @"Pike should have defended successfully");

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
    
    CombatOutcome outcome = [_manager resolveCombatBetween:attacker defender:defender];
    
    STAssertTrue(IsAttackSuccessful(outcome), @"Attack should be successful");
    
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
    
    [_manager resolveCombatBetween:attacker defender:defender1];
    
    STAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");

    [_manager resolveCombatBetween:attacker defender:defender2];

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
    
    [_manager resolveCombatBetween:attacker defender:defender1];
    
    STAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");
    
    [_manager endTurn];
    
    [_manager resolveCombatBetween:attacker defender:defender2];
    
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

    TimedBonus *timedBonus = [[TimedBonus alloc] initWithValue:2 forNumberOfRounds:2];
    [attacker.attack addTimedBonus:timedBonus];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 3, @"Attack lower value should be 3");
    
    [_manager endTurn];
    [_manager endTurn];
    
    STAssertTrue([attacker.attack calculateValue].lowerValue == 3, @"Attack lower value should be 3");

    [_manager endTurn];
    [_manager endTurn];

    STAssertTrue([attacker.attack calculateValue].lowerValue == 5, @"Attack lower value should be 5");
}

@end
