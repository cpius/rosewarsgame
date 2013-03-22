//
//  ImproveWeapons.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "ImproveWeapons.h"

@implementation ImproveWeapons

- (void)startTimedAbility {
    
    [self.card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:3]];
    [self.card.defence addTimedBonus:[[TimedBonus alloc] initWithValue:1]];
}

- (BOOL)friendlyAbility {
    
    return YES;
}

@end
