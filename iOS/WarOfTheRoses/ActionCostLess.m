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

- (void)startTimedAbility {
    
    [super startTimedAbility];
    
    _originalAttackActionCost = self.card.attackActionCost;
    _originalMoveActionCost = self.card.moveActionCost;
    
    self.card.moveActionCost = 0;
    self.card.attackActionCost = 0;
}

- (void)stopTimedAbility {
    
    [super stopTimedAbility];
    
    self.card.moveActionCost = _originalMoveActionCost;
    self.card.attackActionCost = _originalAttackActionCost;
}

- (BOOL)friendlyAbility {
    
    return YES;
}

- (AbilityTypes)abilityType {
    
    return kAbilityActionCoseLess;
}

@end
