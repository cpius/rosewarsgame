//
//  SpecialUnitTest.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import <XCTest/XCTest.h>

#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"

@class GameManager;
@class StandardBattleStrategy;
@interface SpecialUnitTest : XCTestCase {
    
    GameManager *_manager;
    
    StandardBattleStrategy *_battleStrategy;

    FixedDiceStrategy *_attackerFixedStrategy;
    FixedDiceStrategy *_defenderFixedStrategy;
}

@end
