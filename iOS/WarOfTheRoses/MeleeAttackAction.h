//
//  AttackAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "Action.h"

@interface MeleeAttackAction : Action

@property (nonatomic, strong) id<BattleStrategy> battleStrategy;
@property (nonatomic, assign) MeleeAttackTypes meleeAttackType;
@property (nonatomic, assign) CombatOutcome combatOutcome;
@property (nonatomic, readonly) GridLocation *startLocation;

@end
