//
//  ImproveWeapons.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/19/13.
//
//

#import "ImproveWeapons.h"

@implementation ImproveWeapons

- (void)applyEffect {
    
    [self.card.attack addTimedBonus:[[TimedBonus alloc] initWithValue:3 gamemanager:self.card.gamemanager]];
    [self.card.defence addTimedBonus:[[TimedBonus alloc] initWithValue:1 gamemanager:self.card.gamemanager]];
}

- (void)startTimedAbility {
    
    [super startTimedAbility];
    [self applyEffect];
}

- (void)reactivateTimedAbility {
    
    [super reactivateTimedAbility];
    [self applyEffect];
}

- (void)stopTimedAbility {
    
    [super stopTimedAbility];
}

- (BOOL)friendlyAbility {
    
    return YES;
}

- (AbilityTypes)abilityType {
    
    return kAbilityImprovedWeapons;
}

@end
