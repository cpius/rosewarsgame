//
//  RangedAttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/17/13.
//
//

#import "RangedAttackAction.h"

@implementation RangedAttackAction

- (BOOL)isWithinRange {
    
    return self.path.count - 1 <= self.cardInAction.range;
}

@end
