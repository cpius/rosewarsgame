//
//  HKSecondaryAttackDiceRolls.m
//  RoseWars
//
//  Created by Heine Kristensen on 04/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import "HKSecondaryAttackDiceRolls.h"
#import "FixedDiceStrategy.h"

@implementation HKSecondaryAttackDiceRolls

- (instancetype)initWithAttackRoll:(id<DiceStrategy>)attackRoll andDefenseRoll:(id<DiceStrategy>)defenseRoll {
    
    self = [super init];
    if (self) {
        _attackRoll = attackRoll;
        _defenseRoll = defenseRoll;
    }
    
    return self;
}

@end
