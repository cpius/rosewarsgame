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

+ (BasePathFinderStrategy *)getStrategyFromCard:(Card *)fromCard toCard:(Card*)toCard myColor:(PlayerColors)myColor {
    
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

@end
