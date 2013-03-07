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
    
    _originalAttackActionCost = _card.attackActionCost;
    _originalMoveActionCost = _card.moveActionCost;
    
    _card.moveActionCost = 0;
    _card.attackActionCost = 0;
}

- (void)stopTimedAbility {
    
    [super stopTimedAbility];
    
    _card.moveActionCost = _originalMoveActionCost;
    _card.attackActionCost = _originalAttackActionCost;
}

@end
