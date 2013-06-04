//
//  CoolDown.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/21/13.
//
//

#import "CoolDown.h"
#import "CardPool.h"

@implementation CoolDown

- (void)applyEffect {
        
    CCLOG(@"Card: %@ has cooldown", self.card);
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
        
    CCLOG(@"Card: %@ ended cooldown", self.card);
    [super stopTimedAbility];
}

- (BOOL)allowPerformAction:(Action *)action {
    
    // When affected by cooldown, no actions are allowed
    return NO;
}

- (AbilityTypes)abilityType {
    
    return kAbilityCoolDown;
}

@end
