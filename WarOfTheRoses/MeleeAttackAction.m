//
//  AttackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import "MeleeAttackAction.h"

@implementation MeleeAttackAction

- (BOOL)isWithinRange {
    
    return self.path.count - 1 <= self.cardInAction.movesRemaining;
}

@end
