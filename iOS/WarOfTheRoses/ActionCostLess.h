//
//  ActionCostLess.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/6/13.
//
//

#import "TimedAbility.h"

@interface ActionCostLess : TimedAbility {
    
    NSInteger _originalMoveActionCost;
    NSInteger _originalAttackActionCost;
}

@end
