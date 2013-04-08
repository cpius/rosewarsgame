//
//  BattlePlan.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"

@class MeleeAttackAction;
@interface BattlePlan : NSObject

@property (nonatomic, readonly) NSArray *moveActions;
@property (nonatomic, readonly) NSArray *meleeActions;
@property (nonatomic, readonly) NSArray *rangeActions;
@property (nonatomic, readonly) NSArray *abilityActions;

- (NSArray*)createBattlePlanForCard:(Card*)card friendlyUnits:(NSArray*)friendlyUnits enemyUnits:(NSArray*)enemyUnits unitLayout:(NSDictionary*)unitLayout;
- (Action*)getActionToGridLocation:(GridLocation*)gridLocation;

- (NSDictionary *)getAttackDirectionsAction:(MeleeAttackAction*)action withUnitLayout:(NSDictionary*)unitLayout;

@end
