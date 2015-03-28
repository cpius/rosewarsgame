//
//  ShortestPath.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 1/31/13.
//
//

#import <Foundation/Foundation.h>
#import "PathFinderStep.h"
#import "PathFinderStrategy.h"
#import "Card.h"

@class MeleeAttackAction;
@class RangedAttackAction;
@class MoveAction;
@interface PathFinder : NSObject {
    
    NSMutableArray *_openSteps;
    NSMutableArray *_closedSteps;
}

- (instancetype)initWithGameManager:(GameManager*)gamemanager;

- (NSArray *)getPathForCard:(Card*)card fromGridLocation:(GridLocation*)fromLocation toGridLocation:(GridLocation*)toLocation usingStrategy:(id<PathFinderStrategy>)strategy;

- (MoveAction*)getMoveActionFromLocation:(GridLocation*)fromLocation forCard:(Card*)card toLocation:(GridLocation*)toLocation enemyUnits:(NSArray*)enemyUnits;
- (NSArray*)getMoveActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits;

- (MeleeAttackAction*)getMeleeAttackActionForCard:(Card*)card againstEnemyUnit:(Card*)enemyUnit;
- (NSArray*)getMeleeAttackActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits;

- (RangedAttackAction*)getRangedAttackActionForCard:(Card*)card againstEnemyUnit:(Card*)enemyUnit;
- (NSArray*)getRangedAttackActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card enemyUnits:(NSArray*)enemyUnits;

- (NSArray*)getAbilityActionsFromLocation:(GridLocation*)fromLocation forCard:(Card*)card friendlyUnits:(NSArray*)friendlyUnits enemyUnits:(NSArray*)enemyUnits;

@end
