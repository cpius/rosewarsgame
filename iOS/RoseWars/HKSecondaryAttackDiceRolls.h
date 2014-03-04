//
//  HKSecondaryAttackDiceRolls.h
//  RoseWars
//
//  Created by Heine Kristensen on 04/03/14.
//  Copyright (c) 2014 Heine Skov Kristensen. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "DiceStrategy.h"

@interface HKSecondaryAttackDiceRolls : NSObject

@property (nonatomic, readonly) id<DiceStrategy> attackRoll;
@property (nonatomic, readonly) id<DiceStrategy> defenseRoll;

- (instancetype)initWithAttackRoll:(id<DiceStrategy>)attackRoll andDefenseRoll:(id<DiceStrategy>)defenseRoll;

@end
