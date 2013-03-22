//
//  CoolDown.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/21/13.
//
//

#import "TimedAbility.h"

@interface CoolDown : TimedAbility {
    
    NSInteger _originalMoveActionCost;
    NSInteger _originalAttackActionCost;
}

@end
