//
//  CombatTest.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import <SenTestingKit/SenTestingKit.h>
#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"

@class GameManager;
@interface CombatTest : SenTestCase {
    
    GameManager *_manager;
    
    FixedDiceStrategy *_attackerFixedStrategy;
    FixedDiceStrategy *_defenderFixedStrategy;
    
    FixedDeckStrategy *_attackerFixedDeckStrategy;
    FixedDeckStrategy *_defenderFixedDeckStrategy;
}

@end
