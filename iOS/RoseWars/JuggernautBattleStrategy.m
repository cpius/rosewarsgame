//
//  JuggernautBattleStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/27/13.
//
//

#import "JuggernautBattleStrategy.h"

@implementation JuggernautBattleStrategy

+ (id)strategy {
    
    return [[JuggernautBattleStrategy alloc] init];
}

- (BattleResult*)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager {
    
    BattleResult *battleResult = [super resolveCombatBetweenAttacker:attacker defender:defender gameManager:manager];
    
    CombatOutcome outcome;
    
    // Check attackroll
    if (_attackRoll <= _attackValue) {
        outcome = kCombatOutcomePush;
    }
    else {
        outcome = kCombatOutcomeDefendSuccessfulMissed;
    }
    
    if (IsPushSuccessful(outcome)) {
        NSLog(@"Push successful");
    }
    
    [attacker combatFinishedAgainstDefender:defender withOutcome:outcome];
    [defender combatFinishedAgainstAttacker:attacker withOutcome:outcome];
    
    battleResult.combatOutcome = outcome;
    
    return battleResult;
}

@end
