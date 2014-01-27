//
//  StandardBattleStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import "StandardBattleStrategy.h"

@implementation StandardBattleStrategy

+ (id)strategy {
    
    return [[StandardBattleStrategy alloc] init];
}

- (BattleResult*)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager {
    
    BattleResult *battleResult = [super resolveCombatBetweenAttacker:attacker defender:defender gameManager:manager];
    
    CombatOutcome outcome;
    
    // Check attackroll
    if (_attackRoll >= _attackValue.lowerValue && _attackRoll <= _attackValue.upperValue) {
        // Check defenceroll
        if (_defenseRoll >= _defendValue.lowerValue && _defenseRoll <= _defendValue.upperValue) {
            outcome = kCombatOutcomeDefendSuccessful;
        }
        else {
            outcome = kCombatOutcomeAttackSuccessful;
        }
    }
    else {
        outcome = kCombatOutcomeDefendSuccessfulMissed;
    }
    
    if (IsAttackSuccessful(outcome)) {
        NSLog(@"Attack successful");
        [manager attackSuccessfulAgainstCard:defender];
    }
    else {
        NSLog(@"Defend successful");
    }
    
    [attacker combatFinishedAgainstDefender:defender withOutcome:outcome];
    [defender combatFinishedAgainstAttacker:attacker withOutcome:outcome];
    
    battleResult.combatOutcome = outcome;
    
    return battleResult;
}

@end
