//
//  WarElephantBattleStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import "WarElephantBattleStrategy.h"

@implementation WarElephantBattleStrategy

+ (id)strategy {
    
    return [[WarElephantBattleStrategy alloc] init];
}

- (CombatOutcome)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager {
    
    [attacker combatStartingAgainstDefender:defender];
    [defender combatStartingAgainstAttacker:attacker];
    
    [manager.delegate combatHasStartedBetweenAttacker:attacker andDefender:defender];
        
    AttributeRange attackValue = [attacker.attack calculateValue];
    AttributeRange defendValue = [defender.defence calculateValue];
    
    CCLOG(@"Attack value: %@", AttributeRangeToNSString(attackValue));
    CCLOG(@"Defend value: %@", AttributeRangeToNSString(defendValue));
    
    NSUInteger attackRoll = [self.attackerDiceStrategy rollDiceWithDie:6];
    NSUInteger defenceRoll = [self.defenderDiceStrategy rollDiceWithDie:6];
    
    CCLOG(@"Attack roll: %d", attackRoll);
    CCLOG(@"Defence roll: %d", defenceRoll);
    
    CombatOutcome outcome;
    
    // Check attackroll
    if (attackRoll >= attackValue.lowerValue && attackRoll <= attackValue.upperValue) {
        // Check defenceroll
        if (defenceRoll >= defendValue.lowerValue && defenceRoll <= defendValue.upperValue) {
            outcome = kCombatOutcomePush;
        }
        else {
            outcome = kCombatOutcomeAttackSuccessful;
        }
    }
    else {
        outcome = kCombatOutcomeDefendSuccessfulMissed;
    }
    
    if (IsAttackSuccessful(outcome)) {
        CCLOG(@"Attack successful");
        [manager cardHasBeenDefeated:defender];
        [manager.delegate cardHasBeenDefeatedInCombat:defender];
    }
    
    [attacker combatFinishedAgainstDefender:defender withOutcome:outcome];
    [defender combatFinishedAgainstAttacker:attacker withOutcome:outcome];
    
    return outcome;
}

@end
