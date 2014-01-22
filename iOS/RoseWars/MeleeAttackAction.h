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
@property (nonatomic, strong) BattleResult *battleResult;
@property (nonatomic, strong) NSMutableDictionary *secondaryActionsForPlayback;

- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard;
- (id)initWithPath:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard meleeAttackType:(MeleeAttackTypes)meleeAttackType;

@end
