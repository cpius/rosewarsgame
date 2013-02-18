//
//  AIStrategyAdvancer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import "AIStrategyAdvancer.h"
#import "PathFinderStep.h"

@implementation AIStrategyAdvancer

- (Action *)decideNextActionFromBattlePlans:(NSDictionary *)battlePlans {
    
    Action *action = nil;
    BOOL actionFound = NO;
    
    CCLOG(@"Deciding next action");
    
    while (!actionFound) {
        NSUInteger randomKeyIndex = arc4random() % (battlePlans.allKeys.count - 1);
        
        BattlePlan *battlePlanForUnit = [battlePlans objectForKey:[battlePlans.allKeys objectAtIndex:randomKeyIndex]];
        
        if (battlePlanForUnit.moveActions.count > 0) {
            action = [battlePlanForUnit.moveActions objectAtIndex:(arc4random() % (battlePlanForUnit.moveActions.count - 1))];
            
            GridLocation *startLocation = [action.path[0] location];
            GridLocation *endLocation = [action.path.lastObject location];
            
            if (action.path.count > 1 && ![startLocation isEqual:endLocation]) {
                actionFound = YES;
            }
        }
    }
    
    CCLOG(@"Next action found: %@", action);
    
    return action;
}

@end
