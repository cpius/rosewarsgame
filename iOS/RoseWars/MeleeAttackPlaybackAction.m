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
    
    [super performActionWithCompletion:completion];
}

@end
