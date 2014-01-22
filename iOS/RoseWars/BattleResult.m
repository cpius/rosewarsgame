//
//  BattleResult.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/27/13.
//
//

#import "BattleResult.h"

@implementation BattleResult

- (id)initWithAttacker:(Card*)attacker defender:(Card*)defender {
    
    self = [super init];
    
    if (self) {

        _attackingUnit = attacker;
        _defendingUnit = defender;
    }
    
    return self;
}

+ (id)battleResultWithAttacker:(Card*)attacker defender:(Card*)defender {
    
    return [[BattleResult alloc] initWithAttacker:attacker defender:defender];
}

- (NSString*)battleResultString {
    
    NSString *resultString;
    
    if (IsDefenseSuccessful(self.combatOutcome)) {
        
        if (self.combatOutcome == kCombatOutcomeDefendSuccessfulMissed) {
            resultString = [NSString stringWithFormat:@"Missed! (%d)", self.attackRoll];
        }
        else {
            resultString = [NSString stringWithFormat:@"Unit defended (%d)", self.defenseRoll];
        }
    }
    else if (IsAttackSuccessful(self.combatOutcome)) {
        resultString = [NSString stringWithFormat:@"Attack successful (%d)", self.attackRoll];
    }
    else if (IsPushSuccessful(self.combatOutcome)) {
        resultString = @"Pushed!";
    }
    
    return resultString;
}

- (NSDictionary*)asDictionary {

    NSMutableDictionary *battleresult = [NSMutableDictionary dictionary];
    
    [battleresult setValue:@(_attackRoll) forKey:@"attackroll"];
    [battleresult setValue:@(_defenseRoll) forKey:@"defenseroll"];
    [battleresult setValue:@(_combatOutcome) forKey:@"combatoutcome"];
    [battleresult setValue:@(_meleeAttackType) forKey:@"meleeattacktype"];
    
    [battleresult setObject:[NSDictionary dictionaryWithObjectsAndKeys:@(_attackingUnit.cardLocation.row), @"row", @(_attackingUnit.cardLocation.column), @"column", nil] forKey:@"attackingunit"];

    [battleresult setObject:[NSDictionary dictionaryWithObjectsAndKeys:@(_defendingUnit.cardLocation.row), @"row", @(_defendingUnit.cardLocation.column), @"column", nil] forKey:@"defendingunit"];
    
    return [NSDictionary dictionaryWithDictionary:battleresult];
}

- (void)fromDictionary:(NSDictionary*)dictionary {
    
    _attackRoll = [[dictionary objectForKey:@"attackroll"] integerValue];
    _defenseRoll = [[dictionary objectForKey:@"defenseroll"] integerValue];
    _combatOutcome = [[dictionary objectForKey:@"combatoutcome"] integerValue];
    _meleeAttackType = [[dictionary objectForKey:@"meleeattacktype"] integerValue];
}

@end
