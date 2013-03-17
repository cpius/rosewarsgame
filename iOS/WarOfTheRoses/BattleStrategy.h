//
//  BattleStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"


@protocol BattleStrategy <NSObject>

@required
- (CombatOutcome)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager;
+ (id)strategy;

@end
