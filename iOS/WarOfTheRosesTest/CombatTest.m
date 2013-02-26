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

@implementation CombatTest

- (void)setUp
{
    [super setUp];

    _manager = [GameManager sharedManager];
    
    _attackerFixedStrategy = [FixedDiceStrategy strategy];
    _defenderFixedStrategy = [FixedDiceStrategy strategy];
    
    _attackerFixedDeckStrategy = [FixedDeckStrategy strategy];
    _defenderFixedDeckStrategy = [FixedDeckStrategy strategy];
    
    _manager.attackerDiceStrategy = _attackerFixedStrategy;
    _manager.defenderDiceStrategy = _defenderFixedStrategy;
}

- (void)testSimpleCombatDefenceSucces {
    
    NSMutableDictionary *unitLayout = [[NSMutableDictionary alloc] init];
    
    Archer *attacker = [Archer card];
    Pikeman *defender = [Pikeman card];
    
    [unitLayout setObject:attacker forKey:[GridLocation gridLocationWithRow:3 column:3]];
    [unitLayout setObject:defender forKey:[GridLocation gridLocationWithRow:6 column:3]];
    
    _attackerFixedStrategy.fixedDieValue = 3;
    _defenderFixedStrategy.fixedDieValue = 1;
    
    CombatOutcome outcome = [_manager resolveCombatBetween:attacker defender:defender];
    
    STAssertTrue(outcome == kCombatOutcomeDefendSuccessful, @"Pike should have defended successfully");

    STAssertTrue(!defender.dead, @"Defender isn't dead");
    STAssertTrue(!attacker.dead, @"Attacker isn't dead");
}

- (void)testSimpleCombatAttackSucces {
    
    NSMutableDictionary *unitLayout = [[NSMutableDictionary alloc] init];
    
    Archer *attacker = [Archer card];
    Pikeman *defender = [Pikeman card];
    
    [unitLayout setObject:attacker forKey:[GridLocation gridLocationWithRow:3 column:3]];
    [unitLayout setObject:defender forKey:[GridLocation gridLocationWithRow:6 column:3]];
    
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 4;
    
    CombatOutcome outcome = [_manager resolveCombatBetween:attacker defender:defender];
    
    STAssertTrue(outcome == kCombatOutcomeAttackSuccessful, @"Attack should be successful");
    
    STAssertTrue(defender.dead, @"Defender is dead");
    STAssertTrue(!attacker.dead, @"Attacker isn't dead");
}

- (void)testOnlyOneExperiecePointPerRound {
    
    NSMutableDictionary *unitLayout = [[NSMutableDictionary alloc] init];
    
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    LightCavalry *defender2 = [LightCavalry card];
    
    [unitLayout setObject:attacker forKey:[GridLocation gridLocationWithRow:3 column:3]];
    [unitLayout setObject:defender1 forKey:[GridLocation gridLocationWithRow:6 column:3]];
    [unitLayout setObject:defender2 forKey:[GridLocation gridLocationWithRow:5 column:3]];
        
    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    [_manager resolveCombatBetween:attacker defender:defender1];
    
    STAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");

    [_manager resolveCombatBetween:attacker defender:defender2];

    STAssertTrue(attacker.experience == 1, @"Attacker should not have gained extra XP this round");
}

- (void)testUnitShouldIncreaseInLevelAfterTwoSuccesfulAttacksOverTwoRounds {
    
    NSMutableDictionary *unitLayout = [[NSMutableDictionary alloc] init];
    [_attackerFixedDeckStrategy.fixedCards removeAllObjects];
    [_defenderFixedDeckStrategy.fixedCards removeAllObjects];
    
    Archer *attacker = [Archer card];
    Pikeman *defender1 = [Pikeman card];
    LightCavalry *defender2 = [LightCavalry card];
    
    [unitLayout setObject:attacker forKey:[GridLocation gridLocationWithRow:3 column:3]];
    [unitLayout setObject:defender1 forKey:[GridLocation gridLocationWithRow:6 column:3]];
    [unitLayout setObject:defender2 forKey:[GridLocation gridLocationWithRow:5 column:3]];
    
    [_attackerFixedDeckStrategy.fixedCards addObject:attacker];
    
    _manager.currentGame.myDeck = _manager.currentGame.myDeck = [_attackerFixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0];
    
    [_defenderFixedDeckStrategy.fixedCards removeAllObjects];
    
    [_defenderFixedDeckStrategy.fixedCards addObject:defender1];
    [_defenderFixedDeckStrategy.fixedCards addObject:defender2];
    
    _manager.currentGame.enemyDeck = [_defenderFixedDeckStrategy generateNewDeckWithNumberOfBasicType:0 andSpecialType:0 cardColor:0];

    _attackerFixedStrategy.fixedDieValue = 5;
    _defenderFixedStrategy.fixedDieValue = 5;
    
    [_manager resolveCombatBetween:attacker defender:defender1];
    
    STAssertTrue(attacker.experience == 1, @"Attacker should have gained 1 XP");
    
    [_manager endTurn];
    
    [_manager resolveCombatBetween:attacker defender:defender2];
    
    STAssertTrue(attacker.experience == 2, @"Attacker should have gained 2 XP");
    STAssertTrue(attacker.numberOfLevelsIncreased == 1, @"Attacker should have increased a level");
}

@end
