//
//  ImproveWeapons.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "ImproveWeapons.h"

@implementation ImproveWeapons

- (id)initWithCard:(Card *)card {
    
    self = [super initForNumberOfRounds:1 onCard:card];
    
    if (self) {
    }
    
    return self;
}

- (void)startTimedAbility {
    
    [_card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:3]];
    [_card.defence addTimedBonus:[[TimedBonus alloc] initWithValue:1]];
}

- (BOOL)friendlyAbility {
    
    return YES;
}

@end
