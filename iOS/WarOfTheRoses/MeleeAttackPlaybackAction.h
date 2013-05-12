//
//  MeleeAttackPlaybackAction.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/6/13.
//
//

#import "MeleeAttackAction.h"
#import "BaseBattleStrategy.h"

@interface MeleeAttackPlaybackAction : MeleeAttackAction

@property (nonatomic, strong) id<BattleStrategy> battleStrategy;

@end
