//
//  SpecialUnitTest.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import <SenTestingKit/SenTestingKit.h>

#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"

@class GameManager;
@class StandardBattleStrategy;
@interface SpecialUnitTest : SenTestCase {
    
    GameManager *_manager;
    
    StandardBattleStrategy *_battleStrategy;

    FixedDiceStrategy *_attackerFixedStrategy;
    FixedDiceStrategy *_defenderFixedStrategy;
}

@end
