//
//  PathFinderStrategyFactory.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "PathFinderStrategyFactory.h"
#import "MeleeAttackPathFinderStrategy.h"
#import "RangedAttackPathFinderStrategy.h"
#import "MovePathFinderStrategy.h"

@implementation PathFinderStrategyFactory

+ (id<PathFinderStrategy>)getStrategyFromCard:(Card *)fromCard toCard:(Card*)toCard myColor:(PlayerColors)myColor {
    
    if (toCard != nil && ![toCard isOwnedByPlayerWithColor:myColor]) {
        
        if (fromCard.range > 1) {
            return [RangedAttackPathFinderStrategy strategy];
        }
        else {
            return [MeleeAttackPathFinderStrategy strategy];
        }
    }
    else {
        return [MovePathFinderStrategy strategy];
    }
}

+ (id<PathFinderStrategy>)getMoveStrategy {
    
    return [MovePathFinderStrategy strategy];
}

+ (id<PathFinderStrategy>)getMeleeAttackStrategyWithMeleeAttackType:(MeleeAttackTypes)meleeAttackType {
    
    if (meleeAttackType == kMeleeAttackTypeConquer) {
        return [PathFinderStrategyFactory getMeleeAttackWithConquerStrategy];
    }
    else if (meleeAttackType == kMeleeAttackTypeNormal) {
        return [PathFinderStrategyFactory getMeleeAttackStrategy];
    }
    
    return nil;
}

+ (id<PathFinderStrategy>)getMeleeAttackWithConquerStrategy {
    
    return [MeleeAttackPathFinderStrategy strategyWithMeleeAttackType:kMeleeAttackTypeConquer];
}

+ (id<PathFinderStrategy>)getMeleeAttackStrategy {
    
    return [MeleeAttackPathFinderStrategy strategyWithMeleeAttackType:kMeleeAttackTypeNormal];
}

+ (id<PathFinderStrategy>)getRangedAttackStrategy {
    
    return [RangedAttackPathFinderStrategy strategy];
}

@end
