//
//  AttackAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "Action.h"

@interface MeleeAttackAction : Action

@property (nonatomic, assign) MeleeAttackTypes meleeAttackType;
@property (nonatomic, assign) CombatOutcome combatOutcome;

@end
