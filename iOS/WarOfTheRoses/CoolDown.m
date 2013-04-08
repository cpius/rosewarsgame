//
//  CoolDown.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/21/13.
//
//

#import "CoolDown.h"

@implementation CoolDown

- (void)applyEffect {
    
    self.card.moveActionCost = 10;
    self.card.attackActionCost = 10;
    
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
    
    self.card.moveActionCost = self.card.moveActionCost;
    self.card.attackActionCost = self.card.attackActionCost;
    
    CCLOG(@"Card: %@ ended cooldown", self.card);
    [super stopTimedAbility];
}

- (AbilityTypes)abilityType {
    
    return kAbilityCoolDown;
}

@end
