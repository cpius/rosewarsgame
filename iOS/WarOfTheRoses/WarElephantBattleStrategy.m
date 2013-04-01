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

- (BattleResult*)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager {
    
    BattleResult *battleResult = [BattleResult battleResultWithAttacker:attacker defender:defender];

    [attacker combatStartingAgainstDefender:defender];
    [defender combatStartingAgainstAttacker:attacker];
    
    [manager.delegate combatHasStartedBetweenAttacker:attacker andDefender:defender];
        
    AttributeRange attackValue = [attacker.attack calculateValue];
    AttributeRange defendValue = [defender.defence calculateValue];
    
    CCLOG(@"Attack value: %@", AttributeRangeToNSString(attackValue));
    CCLOG(@"Defend value: %@", AttributeRangeToNSString(defendValue));
    
    NSUInteger attackRoll = [self.attackerDiceStrategy rollDiceWithDie:6];
    NSUInteger defenceRoll = [self.defenderDiceStrategy rollDiceWithDie:6];
    
    battleResult.attackRoll = attackRoll;
    battleResult.defenseRoll = defenceRoll;
    
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
            outcome = kCombatOutcomeAttackSuccessfulAndPush;
        }
    }
    else {
        outcome = kCombatOutcomeDefendSuccessfulMissed;
    }
    
    if (IsAttackSuccessful(outcome)) {
        CCLOG(@"Attack successful");
        [manager attackSuccessfulAgainstCard:defender];
    }
    
    [attacker combatFinishedAgainstDefender:defender withOutcome:outcome];
    [defender combatFinishedAgainstAttacker:attacker withOutcome:outcome];
    
    battleResult.combatOutcome = outcome;
    
    return battleResult;
}

@end
