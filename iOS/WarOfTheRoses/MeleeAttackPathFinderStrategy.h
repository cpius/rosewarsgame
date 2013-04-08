//
//  AttackPathFinderStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/15/13.
//
//

#import <Foundation/Foundation.h>
#import "BasePathFinderStrategy.h"
#import "PathFinderStrategy.h"

@interface MeleeAttackPathFinderStrategy : BasePathFinderStrategy

@property (nonatomic, readonly) MeleeAttackTypes meleeAttackType;

+ (id)strategy;
+ (id)strategyWithMeleeAttackType:(MeleeAttackTypes)attackType;

- (id)initWithMeleeAttackType:(MeleeAttackTypes)meleeAttackType;

@end
