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

- (Action *)decideNextActionFromActions:(NSArray *)actions {
    
    Action *action = nil;
    
    NSLog(@"Deciding next action");
    
    for (Action *action in actions) {
        
        PathFinderStep *startPositionStep = action.path[0];
        GridLocation *startPosition =  startPositionStep.location;
        
        PathFinderStep *endPositionStep = action.path.lastObject;
        GridLocation *endPosition = endPositionStep.location;
        
        action.score = endPosition.row;
        
        if (endPosition.row > startPosition.row) {
            action.score += 0.1;
        }
        
        if (action.isAttack) {
            action.score += 0.25;
        }
    }
    
    action = [[actions sortedArrayUsingComparator:^NSComparisonResult(id obj1, id obj2) {
        
        Action *action1 = obj1;
        Action *action2 = obj2;
        
        return action1.score > action2.score;
    }] lastObject];
    
    NSLog(@"Next action found: %@", action);
    
    return action;
}

@end
