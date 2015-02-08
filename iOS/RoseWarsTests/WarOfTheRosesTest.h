//
//  WarOfTheRosesTest.h
//  WarOfTheRosesTest
//
//  Created by Heine Skov Kristensen on 2/16/13.
//
//

#import <XCTest/XCTest.h>
#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"

@class GameManager;
@interface WarOfTheRosesTest : XCTestCase {
    
    
    FixedDiceStrategy *_attackerFixedStrategy;
    FixedDiceStrategy *_defenderFixedStrategy;
}

@end
