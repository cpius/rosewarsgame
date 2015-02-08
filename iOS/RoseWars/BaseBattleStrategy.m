//
//  BaseBattleStrategy.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import "BaseBattleStrategy.h"
#import "RandomDiceStrategy.h"
#import "BattleResult.h"

@implementation BaseBattleStrategy

@synthesize attackerDiceStrategy = _attackerDiceStrategy;
@synthesize defenderDiceStrategy = _defenderDiceStrategy;

- (id)init {
    
    self = [super init];
    
    if (self) {
        
        self.attackerDiceStrategy = [RandomDiceStrategy strategy];
        self.defenderDiceStrategy = [RandomDiceStrategy strategy];
    }
    
    return self;
}

- (BattleResult*)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager {
    
    BattleResult *battleResult = [BattleResult battleResultWithAttacker:attacker defender:defender];
    
    [attacker combatStartingAgainstDefender:defender];
    [defender combatStartingAgainstAttacker:attacker];
    
    [manager.delegate combatHasStartedBetweenAttacker:attacker andDefender:defender];
    
    _attackValue = [attacker.attack calculateValue];
    _defendValue = [defender.defence calculateValue];
    
    // Adjust defense if attack is greater than 1-6
    if (_attackValue.lowerValue < 1) {
        _defendValue.upperValue--;
    }
    
    NSLog(@"Attack value: %@", AttributeRangeToNSString(_attackValue));
    NSLog(@"Defend value: %@", AttributeRangeToNSString(_defendValue));
    
    _attackRoll = [attacker.battleStrategy.attackerDiceStrategy rollDiceWithDie:6];//[self.attackerDiceStrategy rollDiceWithDie:6];
    _defenseRoll = [defender.battleStrategy.defenderDiceStrategy rollDiceWithDie:6];//[self.defenderDiceStrategy rollDiceWithDie:6];
    
    battleResult.attackRoll = _attackRoll;
    battleResult.defenseRoll = _defenseRoll;
    
    NSLog(@"Attack roll: %ld", (long)_attackRoll);
    NSLog(@"Defence roll: %ld", (long)_defenseRoll);
    
    return battleResult;
}

+ (id)strategy {
    
    @throw [NSException exceptionWithName:@"Error" reason:@"Musn't call strategy on baseclass" userInfo:nil];
}

@end
