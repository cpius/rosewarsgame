//
//  MoveTest.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/26/13.
//
//

#import <XCTest/XCTest.h>
#import "FixedDiceStrategy.h"
#import "FixedDeckStrategy.h"

@class GameManager;
@interface MoveTest : XCTestCase {
    
    FixedDiceStrategy *_attackerFixedStrategy;
    FixedDiceStrategy *_defenderFixedStrategy;
}

@end
