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
    
    self.cardInAction.battleStrategy = _battleStrategy;
    
    if (self.meleeAttackType == kMeleeAttackTypeConquer) {
        self.autoConquer = YES;
    }
    
    [super performActionWithCompletion:completion];
}

@end
