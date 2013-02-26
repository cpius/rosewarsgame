//
//  AIStrategyDestroyer.m
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/23/13.
//
//

/*
 
 def get_action(p, actions, document_it = False):
 
 for action in actions:
 if action.is_attack:
 chance = m.chance_of_win(action.unit, action.enemy_unit, action)
 action.score = chance * 10
 if hasattr(action.unit, "double_attack_cost"):
 action.score = action.score / 2
 else:
 action.score = 0
 
 if action.is_ability:
 action.score = 8
 
 
 if hasattr(action, "push"):
 action.score = 10
 
 rnd.shuffle(actions)
 actions.sort(key = attrgetter("score"), reverse= True)
 if document_it:
 m.document_actions("Destroyer", actions, p)
 return actions[0]

 
*/

#import "AIStrategyDestroyer.h"
#import "PathFinderStep.h"

@interface AIStrategyDestroyer()

- (float)chanceOfAttacker:(Card*)attacker winningOverDefender:(Card*)defencer withAction:(Action*)action;

@end

@implementation AIStrategyDestroyer

- (Action *)decideNextActionFromActions:(NSArray *)actions {
    
    Action *action = nil;
    
    CCLOG(@"Deciding next action");
    
    for (Action *action in actions) {
        
        GridLocation *startPosition = [action.path[0] location];
        GridLocation *endPosition = [action.path.lastObject location];
        
        if (action.isAttack) {
            action.score = [self chanceOfAttacker:action.cardInAction winningOverDefender:action.enemyCard withAction:action] * 10;
        }
    }
    
    action = [[actions sortedArrayUsingComparator:^NSComparisonResult(id obj1, id obj2) {
        
        Action *action1 = obj1;
        Action *action2 = obj2;
        
        return action1.score > action2.score;
    }] lastObject];
    
    CCLOG(@"Next action found: %@", action);
    
    return action;
}

- (float)chanceOfAttacker:(Card *)attacker winningOverDefender:(Card *)defencer withAction:(Action *)action {
    
    NSUInteger attackValue = MIN(MAX([attacker.attack calculateValue].upperValue, 0), 6);
    NSUInteger defendValue = MIN(MAX([defencer.defence calculateValue].upperValue, 0), 6);
    
    return ((7- attackValue) / 6) * ((6 - defendValue) / 6);
}

@end
