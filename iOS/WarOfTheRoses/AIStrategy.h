//
//  AIStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/18/13.
//
//

#import <Foundation/Foundation.h>
#import "Action.h"
#import "BattlePlan.h"

@protocol AIStrategy <NSObject>

- (Action *)decideNextActionFromActions:(NSArray *)actions;

@end
