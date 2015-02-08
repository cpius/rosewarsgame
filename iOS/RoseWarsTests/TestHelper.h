//
//  TestHelper.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import <Foundation/Foundation.h>
#import "Definitions.h"

@class Game;
@interface TestHelper : NSObject {

}

+ (void)swapBoardInGame:(Game*)game myCurrentGameBoardSide:(GameBoardSides)gameBoardSide;
+ (Game *)setupGame:(Game*)game gamemanager:(GameManager*)gamemanager withPlayer1Units:(NSArray *)player1Units player2Units:(NSArray *)player2Units;

@end
