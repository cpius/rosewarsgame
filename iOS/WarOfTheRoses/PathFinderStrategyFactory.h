//
//  PathFinderStrategyFactory.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <Foundation/Foundation.h>
#import "PathFinderStrategy.h"
#import "Card.h"

@interface PathFinderStrategyFactory : NSObject

+ (id<PathFinderStrategy>)getStrategyFromCard:(Card *)fromCard toCard:(Card*)toCard myColor:(PlayerColors)myColor;

+ (id<PathFinderStrategy>)getMoveStrategy;
+ (id<PathFinderStrategy>)getMeleeAttackWithConquerStrategy;
+ (id<PathFinderStrategy>)getMeleeAttackStrategy;
+ (id<PathFinderStrategy>)getMeleeAttackStrategyWithMeleeAttackType:(MeleeAttackTypes)meleeAttackType;
+ (id<PathFinderStrategy>)getRangedAttackStrategy;

@end
