//
//  ActionCostLess.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/6/13.
//
//

#import "ActionCostLess.h"
#import "Card.h"

@implementation ActionCostLess

- (void)applyEffect {
    
    _originalAttackActionCost = self.card.attackActionCost;
    _originalMoveActionCost = self.card.moveActionCost;
    
    self.card.moveActionCost = 0;
    self.card.attackActionCost = 0;
}

- (void)reactivateTimedAbility {
    
    [super reactivateTimedAbility];
    [self applyEffect];
}

- (void)startTimedAbility {
    
    [super startTimedAbility];
    [self applyEffect];
}

- (void)stopTimedAbility {
    
    self.card.moveActionCost = _originalMoveActionCost;
    self.card.attackActionCost = _originalAttackActionCost;

    [super stopTimedAbility];
}

- (BOOL)friendlyAbility {
    
    return YES;
}

- (AbilityTypes)abilityType {
    
    return kAbilityActionCoseLess;
}

@end
