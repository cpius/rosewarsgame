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
    
    @throw [NSException exceptionWithName:@"Error" reason:@"Musn't call resolveCombatBetween:(Card *)attacker defender:(Card *)defender on baseclass" userInfo:nil];
}

+ (id)strategy {
    
    @throw [NSException exceptionWithName:@"Error" reason:@"Musn't call strategy on baseclass" userInfo:nil];
}

@end
