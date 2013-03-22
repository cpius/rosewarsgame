//
//  CoolDown.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/21/13.
//
//

#import "CoolDown.h"

@implementation CoolDown

- (void)startTimedAbility {
    
    [super startTimedAbility];
    
    _originalAttackActionCost = self.card.attackActionCost;
    _originalMoveActionCost = self.card.moveActionCost;
    
    self.card.moveActionCost = 10;
    self.card.attackActionCost = 10;
    
    CCLOG(@"Card: %@ has cooldown", self.card);
}

- (void)stopTimedAbility {
    
    [super stopTimedAbility];
    
    self.card.moveActionCost = _originalMoveActionCost;
    self.card.attackActionCost = _originalAttackActionCost;
    
    CCLOG(@"Card: %@ ended cooldown", self.card);
}
@end
