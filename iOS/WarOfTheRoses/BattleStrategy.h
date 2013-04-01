//
//  BattleStrategy.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 3/15/13.
//
//

#import <Foundation/Foundation.h>
#import "Card.h"
#import "BattleResult.h"

@protocol BattleStrategy <NSObject>

@required
- (BattleResult*)resolveCombatBetweenAttacker:(Card *)attacker defender:(Card *)defender gameManager:(GameManager*)manager;
+ (id)strategy;

@end
