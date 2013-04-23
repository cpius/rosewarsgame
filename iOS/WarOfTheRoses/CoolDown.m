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
    
    Card *originalCard = [CardPool createCardOfName:self.card.unitName];
    
    self.card.moveActionCost = originalCard.moveActionCost;
    self.card.attackActionCost = originalCard.attackActionCost;
    
    CCLOG(@"Card: %@ ended cooldown", self.card);
    [super stopTimedAbility];
}

- (AbilityTypes)abilityType {
    
    return kAbilityCoolDown;
}

@end
