//
//  TestHelper.h
//  WarOfTheRoses
//
//  Created by Heine Skov Kristensen on 2/27/13.
//
//

#import <Foundation/Foundation.h>

@class Game;
@interface TestHelper : NSObject {

}


+ (Game *)setupGame:(Game*)game withPlayer1Units:(NSArray *)player1Units player2Units:(NSArray *)player2Units;

@end
