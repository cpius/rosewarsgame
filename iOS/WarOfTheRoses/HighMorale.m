//
//  HighMorale.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/5/13.
//
//

#import "HighMorale.h"

@implementation HighMorale

- (void)startTimedAbility {
    
    [super startTimedAbility];
    
}

- (void)stopTimedAbility {
    
    [super stopTimedAbility];
    
}

- (BOOL)friendlyAbility {
    
    return YES;
}

- (AbilityTypes)abilityType {
    
    return kAbilityHighMorale;
}

@end
