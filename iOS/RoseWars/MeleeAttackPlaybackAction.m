//
//  MeleeAttackPlaybackAction.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 5/6/13.
//
//

#import "MeleeAttackPlaybackAction.h"

@implementation MeleeAttackPlaybackAction

- (void)performActionWithCompletion:(void (^)())completion {
        
    if (self.meleeAttackType == kMeleeAttackTypeConquer) {
        self.meleeAttackStrategy = kMeleeAttackStrategyAutoConquer;
    }
    
    [super performActionWithCompletion:completion];
}

@end
