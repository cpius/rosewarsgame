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
@property (nonatomic, assign) MeleeAttackStrategy meleeAttackStrategy;
@property (nonatomic, readonly) GridLocation *gridLocationForConquer;


- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard;
- (id)initWithGameManager:(GameManager*)gamemanager path:(NSArray *)path andCardInAction:(Card *)card enemyCard:(Card *)enemyCard meleeAttackType:(MeleeAttackTypes)meleeAttackType;

- (BOOL)unitCanConquerEnemyLocation;
- (void)conquerEnemyLocationWithCompletion:(void (^)())completion;

@end
